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
    # initialize teritory serializer
    territory = TerritorySerializer()
    # initialize teritory serializer
    currency = CurrencySerializer()

    def create(self, validated_data):
        '''
        custom create function
        '''
        # get the currency inputs
        currency_data = validated_data.pop("currency")
        # get the territory inputs
        territory_data = validated_data.pop("territory")
        # create currency if not exists
        currency_obj, created = models.Currency.objects.get_or_create(
                                    **currency_data
                                    )
        # create territory if not exists
        territory_obj, created = models.Territory.objects.get_or_create(
                                    local_currency=currency_obj,
                                    **territory_data
                                    )
        # create DSR if not exists
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
    # initialize DSR serializer
    dsr = DSRSerializer()

    def create(self, validated_data):
        '''
        custom create function
        '''
        # get the dsr id
        dsr_id = validated_data.pop('dsr')
        # create a resource object
        resource_obj = models.Resource.objects.create(
                        dsr_id = dsr_id,
                        **validated_data
                        )
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
