from marshmallow import Schema


class ReducedSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("hash_id", "name", "status")
        ordered = True


class ImageSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("original", "small", "medium", "large")
        ordered = True
