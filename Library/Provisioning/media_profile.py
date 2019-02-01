from base import Base


class MediaProfile(Base):

    def __init__(self, **kwargs):
        super(MediaProfile, self).__init__(**kwargs)

    def create_media_profile(self, **kwargs):
        label = "MediaProfile.create_media_profile"
        name = kwargs.get("name", None)
        response = self.create_entity(url="URL1",
                                      data_frame="media-profile-data",
                                      to_create={"attributes": {"name__s": name}})
        if response == 409:
            media_profiles = self.get_entities(url="URL1", filter_="auxiliaryDataList")
            names = self.lookup_key(field="name__s", data=media_profiles)
            try:
                index = names.index(name)
                if index:
                    media_profile = media_profiles[0][index]
                    if media_profile:
                        self.delete_media_profile(id_=media_profile.get("id"))
                        response = self.create_media_profile(name=name)
            except ValueError as error_:
                self.print_message(message=str(error_),
                                   function=label,
                                   type_="error")
        return response

    def delete_media_profile(self, **kwargs):
        id_ = kwargs.get("id_", None)
        return self.delete_entity(url="URL1",
                                  id_=id_)

# test = MediaProfile()
# print(test.create_media_profile(name="ravipr2"))
# test.delete_media_profile(id_="AWiatQ1TA7316vGBC_r9")
