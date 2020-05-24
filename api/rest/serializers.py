from rest_framework import serializers
from rest import models
from rest.enum_classes import ListColor
from rest.host_blocker import HostBlocker


class ManagelistColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ManageList
        fields = ['color']


class HostSerializer(serializers.ModelSerializer):
    on_list = serializers.SerializerMethodField()

    class Meta:
        model = models.Host
        fields = serializers.ALL_FIELDS

    def get_on_list(self, obj):
        list = models.ManageList.objects.filter(host_id=obj.id)
        return list.get().color if list.exists() else "No"


class ThreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Threat
        fields = serializers.ALL_FIELDS
        depth = 1


class StatsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Stats
        fields = serializers.ALL_FIELDS
        depth = 1


class BlackListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ManageList
        fields = ['id', 'host', 'reason', 'time_added']

    def validate_color(self, value):
        if value != ListColor.BLACK.value:
            raise serializers.ValidationError('It is not blacklist entry')
        return value

    def create(self, validated_data):
        blocker = HostBlocker()
        query = models.Host.objects.filter(id=validated_data['host'].id)
        if query.exists():
            host = query.get()
            host.blocked = True
            host.save()
            blocker.block_host(host.original_ip)
        return models.ManageList.objects.create(host_id=validated_data['host'].id,
                                                reason=validated_data['reason'],
                                                color=ListColor.BLACK.value)


class WhiteListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ManageList
        fields = ['id', 'host', 'reason', 'time_added']

    def validate_color(self, value):
        if value != ListColor.WHITE.value:
            raise serializers.ValidationError('it is not whitelist entry')
        return value

    def create(self, validated_data):
        return models.ManageList.objects.create(host_id=validated_data['host'].id,
                                                reason=validated_data['reason'],
                                                color=ListColor.WHITE.value)
