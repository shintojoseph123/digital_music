# lib imports
import os
import json
import pycountry
import pandas as pd
from pathlib import Path
from tablib import Dataset
from datetime import datetime
# django imports
from django.shortcuts import render
# django rest imports
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
# file imports
from dsrs import models, serializers
from dsrs.resources import ResourceResource


def ingest(request):
    # initialize a dict
    context=dict()
    # if POST method
    if request.method == 'POST':
        # get folder path
        folder_path = request.POST['folder_path']
        # initialize Dataset
        dataset = Dataset()
        # initialize ResourceResource
        resource_resource = ResourceResource()
        # intitialize DSR serializer
        dsr = serializers.DSRSerializer()
        # current file path
        dir_path = os.path.dirname(os.path.realpath(__file__))
        # merging folder path
        folder_path = dir_path + folder_path
        # files with .gz extension
        pathlist = Path(folder_path).rglob('*.gz')
        # data insertion status
        ingestion_status = dict()
        # for each file in pathlist
        for file_path in pathlist:
            # get the file name
            file_name = file_path.stem
            # convert filepath into string
            file_path = str(file_path)
             # read datat from file
            df = pd.read_csv(file_path,  sep="\t", compression='gzip')
            # remove file extension
            file_name_list = file_name.split('.')[0].split('_')
            # get date range
            date_range = file_name_list[-1].split('-')
            # get currency info
            currency_info = pycountry.currencies.get(alpha_3=file_name_list[-2])
            # get territory info
            territory_info = pycountry.countries.get(alpha_2=file_name_list[-3])
            # create DSR data
            dsr_data = {
            	'path': file_path,
            	'period_end': datetime.strptime(date_range[1], '%Y%m%d'),
            	'period_start': datetime.strptime(date_range[0], '%Y%m%d'),
                'currency': {
                    'name':currency_info.name,
                    'code':currency_info.alpha_3,
                    'symbol':currency_info.numeric,
                    },
            	'territory': {
                    'name':territory_info.name,
                    'code_2':territory_info.alpha_2,
                    'code_3':territory_info.alpha_3,
                    },
            }
            # create dsr
            dsr_obj = dsr.create(dsr_data)
            # assign DSR id to df
            df['dsr'] = dsr_obj.id
            # convert to json and load
            imported_data = dataset.load(df.to_json(orient='records'))
            # check whether anything is breaking
            result = resource_resource.import_data(dataset, dry_run=True)
            # if not issue insert data
            if not result.has_errors():
                # Actually import now
                resource_resource.import_data(dataset, dry_run=False)
                # status message
                message = "success"
            else:
                # status message
                message = "failed"
            # save status
            ingestion_status[file_name] = message
        # ingestion_status
        context['ingestion_status'] = ingestion_status
    # return rendered html page
    return render(request, "ingest.html", context)



class ResourceViewSet(viewsets.ModelViewSet):
    # queryset
    queryset = models.Resource.objects.all()
    # serializer
    serializer_class = serializers.ResourceSerializer

    def percentile(self, request, number):
        '''
        Calculates TOP percentile by revenue

        Parameters:
            number (str)    : The Percentile.

        Returns:
            list: returns the unique resources by revenue
              that accounts Percentile of the total revenue.
        '''

        # from IPython import embed
        # embed()
        # percentile query
        query = '''
                WITH
                    Percentiles AS (SELECT
                                        id,
                                        revenue,
                                        PERCENT_RANK() OVER(ORDER BY revenue) AS percentile_rank
                                    FROM
                                        resource)
                SELECT *
                FROM
                    Percentiles
                WHERE
                   percentile_rank > %s
                ORDER BY
                   percentile_rank DESC;
                '''% (1- number/100)

        # execute raw query
        query_obj = models.Resource.objects.raw(query)

        for each in query_obj:
            # print (each.id)
            print (each.percentile_rank)
            # print (each.revenue)
            # break

        message = {"message":"Data deleted successfully!"}
        return Response(message, status=status.HTTP_204_NO_CONTENT)



class DSRViewSet(viewsets.ModelViewSet):
    queryset = models.DSR.objects.all()
    serializer_class = serializers.DSRSerializer

    def destroy(self, request, pk):
        instance = self.get_object()
        self.perform_destroy(instance)
        message = {"message":"Data deleted successfully!"}
        return Response(message, status=status.HTTP_204_NO_CONTENT)
