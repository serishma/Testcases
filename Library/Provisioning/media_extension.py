from base import Base

class MediaExtension(Base):

    def __init__(self, **kwargs):
        super(MediaExtension, self).__init__(**kwargs)

    def create_media_extension(self, **kwargs):
        label = "MediaExtension.create_media_extension"
        name = kwargs.get("name", None)
        media_profile = kwargs.get("media_profile", None)
        response = self.create_entity(url="URL2",
                                      data_frame="media-ext-data",
                                      to_create={"attributes": {"name__s": name,
                                                                "mmProfileId__s": self.condition_response(
                                                                    data=media_profile)}})
        if response == 409:
            media_ext_profiles = self.get_entities(url="URL2", filter_="auxiliaryDataList")
            names = self.lookup_key(field="name__s", data=media_ext_profiles)
            try:
                index = names.index(name)
                if index:
                    media_ext_profile = media_ext_profiles[0][index]
                    if media_ext_profile:
                        self.delete_media_extension(id_=media_ext_profile.get("id"))
                        response = self.create_media_extension(name=name, media_profile=media_profile)
            except ValueError as error_:
                self.print_message(message=str(error_),
                                   function=label,
                                   type_="error")

        return response

    def delete_media_extension(self, **kwargs):
        id_ = kwargs.get("id_", None)
        return self.delete_entity(url="URL2",
                                  id_=id_)
