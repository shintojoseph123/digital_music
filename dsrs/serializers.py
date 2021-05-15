from rest_framework import serializers
from dsrs import models


class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Territory
        fields = (
            "name",
            "code_2",
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = (
            "name",
            "code",
        )


class DSRSerializer(serializers.ModelSerializer):
    territory = TerritorySerializer()
    currency = CurrencySerializer()

    def create(self, validated_data):

        currency_data = validated_data.pop("currency")
        territory_data = validated_data.pop("territory")

        currency_obj, created = models.Currency.objects.get_or_create(
                                    **currency_data
                                    )
        territory_obj, created = models.Territory.objects.get_or_create(
                                    local_currency=currency_obj,
                                    **territory_data
                                    )
        dsr_obj, created = models.DSR.objects.get_or_create(
                                currency    = currency_obj,
                                territory   = territory_obj,
                                **validated_data
                                )
        return dsr_obj

    class Meta:
        model = models.DSR
        fields = (
            "id",
            "path",
            "period_end",
            "period_start",
            "territory",
            "currency",
        )



class ResourceSerializer(serializers.ModelSerializer):
    dsr = DSRSerializer()

    def create(self, validated_data):


        # dsr = DSRSerializer()

        dsr_data = validated_data.pop('dsr')
        # create a DSR object
        # dsr_obj = dsr.create(dsr_data)

        # models.DSR.objects.filter(
        #                 id = dsr_obj.id,
        #                 )
        #
        # models.Resource.objects.filter(
        #                 dsr__id = dsr_obj.id,
        #                 )


        resource_obj = models.Resource.objects.create(
                        dsr_id = dsr_data,
                        **validated_data
                        )

        # resource_obj = models.Resource.objects.create(
        #                 dsr_id = dsr_obj.id,
        #                 **validated_data
        #                 )

        # resource_obj = models.Resource.objects.create(
        #                 dsr = dsr_obj,
        #                 **validated_data
        #                 )
        return resource_obj


    class Meta:
        model = models.Resource
        fields = (
            "id",
            "dsp_id",
            "usages",
            "revenue",
            "isrc",
            "title",
            "artists",
            "dsr",
        )
