from base import Base
from time import sleep

class Site(Base):

    def __init__(self, **kwargs):
        super(Site, self).__init__(**kwargs)

    def create_site(self, **kwargs):
        label = "MediaExtension.create_media_extension"
        name = kwargs.get("name", None)
        media_profile = kwargs.get("media_profile", None)
        media_extension = kwargs.get("media_extension", None)
        response = self.create_entity(url="URL3",
                                      data_frame="site-data",
                                      to_create={"attributes": {"name__s": name,
                                                                "mmProfileId__s": self.condition_response(
                                                                    data=media_profile),
                                                                "extMultimediaProfileId__s": self.condition_response(
                                                                    data=media_extension)}})
        if response == 409:
            sites = self.get_entities(url="URL3", filter_="auxiliaryDataList")
            names = self.lookup_key(field="name__s", data=sites)
            try:
                index = names.index(name)
                if index:
                    site = sites[0][index]
                    if site:
                        self.delete_site(id_=site.get("id"))
                        sleep(self.DELAY)
                        response = self.create_site(name=name,
                                                    media_profile=media_profile,
                                                    media_extension=media_extension)
                        sleep(self.DELAY)
            except ValueError as error_:
                self.print_message(message=str(error_),
                                   function=label,
                                   type_="error")

        return response

    def delete_site(self, **kwargs):
        id_ = kwargs.get("id_", None)
        return self.delete_entity(url="URL3",
                                  id_=id_)

    def validate(self, **kwargs):
        site = kwargs.get("site",None)
        xpath = kwargs.get("xpath", "SITE_XPATH")
        attribute = kwargs.get("attribute", "*")
        id_ = self.condition_response(data=site)
        return self.validate_xml(xpath=xpath,
                                 id_=id_,
                                 url_key="URL3",
                                 attribute=attribute)
