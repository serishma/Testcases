# create site ,test id (name),del
from Library1.Provisioning.Provisioning import Provisioning
from Library1.Commonfunctions import Commonfunctions



class CreateSite:

    def __init__(self):
        """
        Constructor fnction for the create_site test case
        """
        self.provisioning = Provisioning()
        self.common_functions = Commonfunctions()
        self.connection_info = {"hostname": "ace103.dev.broadcloudcc.com",
                                "username": "transera",
                                "password": "transera",
                                "database": "provisioning"
                                }
        self.configuration = self.provisioning.open_json()  # get the configuration from the json file

    def test_create_site_003(self, name):
        """
        Create site routine to test the create site functionality
        :return: None
        """
        site_response, media_profile_id, media_extension_id = self.provisioning.create_site(
            name)  # Create the Site and obtain the response
        return site_response, name, media_profile_id, media_extension_id

    def validate_site_003(self, name, tenant, site_sid):
        query = "SELECT * FROM provisioning.site_mst where site_name = '{name}' and tenant_id='{tenant}';".format(
            name=str(name),
            tenant=str(tenant)
        )
        sql_results = self.common_functions.cjp_db_connection_fetching_data \
            (query, self.connection_info)  # get the Site based on the `name`
        # As per the mapping the database ID is the first column -> 0th Index in the SQL result
        # Assuming under single tenant unique ite name exist
        # site_id = sql_result[0][0]

        sites = self.provisioning.get_site()
        if type(sites) == list:
            for site in sites:
                site_id_dbl = site.get("attributes", {"dbId__l", None}).get("dbId__l", None)
                site_sid_db = site["attributes"]["sid"]
                for sql_result in sql_results:
                    site_id_temp = sql_result[0]
                    if site_id_dbl == site_id_temp:
                        if site_sid == site_sid_db:
                            return site

                # if site_id_dbl == site_id:
                #    return site

    def test446(self, name, tenant, do_not_validate=True):
        '''
        valdating site_mst table from DB
        :param name:
        :param tenant:
        :return:
        '''
        create_site, name, media_profile_id, media_extension_id = self.test_create_site_003(name)
        site_sid = create_site[0]["links"][0]["href"].split("/")[-1]
        if do_not_validate:
            validate_site = False
        else:
            validate_site = self.validate_site_003(name, tenant, site_sid)

        # print( create_site)
        # print("-----------------------------")
        # print(validate_site)

        if validate_site:

            site_sid_db = validate_site["attributes"]["sid"]

            if site_sid == site_sid_db:
                message = "[o] Test case (test446) {name} was successful SITE_ID from create = {sid} and DBL_ID ={dbid}".format \
                    (name=str(name),
                     sid=str(site_sid),
                     dbid=str(site_sid_db))
            else:
                message = "[x] Test case (test446) {name} was FAILED SITE_ID from create = {sid} and DBL_ID ={dbid}".format \
                    (name=str(name),
                     sid=str(site_sid),
                     dbid=str(site_sid_db))
            print(message)
        else:
            if do_not_validate is True:
                print("[x] ERROR : Invalid DB data : {data}".format(data=str(validate_site)))

        return create_site, name, media_profile_id, media_extension_id

    def test626_test645(self, name, tenant, create_new=True, println=True, **kwargs):
        if create_new:
            create_site, name, media_profile_id, media_extension_id = self.test446(name, tenant)
        else:
            params = kwargs.get("params")
            create_site = params.get("create_site")
            name = params.get("name")
            media_profile_id = params.get("media_profile_id")
            media_extension_id = params.get("media_extension_id")
        site_sid = create_site[0]["links"][0]["href"].split("/")[-1]

        def print_status(frame, type_, id_):
            import json
            status = json.loads(frame["details"]["reason"])
            if status["deleted"]:
                message = "[o] Deleted {type_} with ID = {id_}"
                print(message.format(type_=str(type_), id_=str(id_)))

        if println:
            print_status(self.provisioning.delete_profile \
                             (media_profile_id,
                              self.provisioning.configuration["DELETE_MEDIA_PROFILE_URL"]),
                         "media-profile",
                         media_profile_id)
            print_status(self.provisioning.delete_profile \
                             (media_extension_id,
                              self.provisioning.configuration["DELETE_MULTIMEDIA_EXT_URL"]),
                         "third-party-profile",
                         media_extension_id)
            print_status(self.provisioning.delete_profile \
                             (site_sid,
                              self.provisioning.configuration["URL3"]),
                         "site",
                         site_sid)

    def test544(self, name, tenant, create_new=True, **kwargs):
        if create_new:
            create_site, name, media_profile_id, media_extension_id = self.test446(name, tenant)
        else:
            params = kwargs.get("params")
            create_site = params.get("create_site")
            name = params.get("name")
            media_profile_id = params.get("media_profile_id")
            media_extension_id = params.get("media_extension_id")

        site_sid = create_site[0]["links"][0]["href"].split("/")[-1]

        update_params = {"longitude__d": 100, "latitude__d": 60}
        site_response = self.provisioning.update_profile("URL3",
                                                         "update-site",
                                                         name,
                                                         site_sid,
                                                         ["X-BSFT-Unique-Constraint"],
                                                         to_update=update_params)
        site_sid = site_response[0]["links"][0]["href"].split("/")[-1]
        site = self.provisioning.get_single_entry("GET_SITE_URL",
                                                  site_sid)
        attributes = site.get("attributes", {})
        params_update_mapping = []
        if attributes:
            for k, v in update_params.items():
                if update_params[k] == attributes[k]:
                    params_update_mapping.append(True)
                else:
                    params_update_mapping.append(False)
            if all(params_update_mapping):
                message = "[o] Test case (test544) {name} UPDATE was successful SITE_ID = {sid}".format \
                    (name=str(name),
                     sid=str(site_sid))
            else:
                message = "[x] Test case (test544) {name} UPDATE was FAILED SITE_ID = {sid}".format \
                    (name=str(name),
                     sid=str(site_sid))
            print(message)
        else:
            print("[x] ERROR update_site failed since site was not retrieved back successfully")

        # self.test626_test645(name, tenant, False, False, params={"create_site": create_site,
        #                                                          "name": name,
        #                                                          "media_profile_id": media_profile_id,
        #                                                          "media_extension_id": media_extension_id})

    def test561(self, name, tenant, create_new=True, **kwargs):
        if create_new:
            create_site, name, media_profile_id, media_extension_id = self.test446(name, tenant)
        else:
            params = kwargs.get("params")
            create_site = params.get("create_site")
            name = params.get("name")
            media_profile_id = params.get("media_profile_id")
            media_extension_id = params.get("media_extension_id")

        update_params = {"description__s": "updated_description"}
        media_profile_response = self.provisioning.update_profile("URL1",
                                                                  "update-media-profile",
                                                                  name,
                                                                  media_profile_id,
                                                                  to_update=update_params)
        media_profile_id = media_profile_response[0]["links"][0]["href"].split("/")[-1]
        site = self.provisioning.get_single_entry("URL1",
                                                  media_profile_id)
        attributes = site.get("attributes", {})
        params_update_mapping = []
        if attributes:
            for k, v in update_params.items():
                if update_params[k] == attributes[k]:
                    params_update_mapping.append(True)
                else:
                    params_update_mapping.append(False)
            if all(params_update_mapping):
                message = "[o] Test case (test561) {name} UPDATE was successful MEDIA_PROFILE_ID = {sid}".format \
                    (name=str(name),
                     sid=str(media_profile_id))
            else:
                message = "[x] Test case (test561) {name} UPDATE was FAILED MEDIA_PROFILE_ID = {sid}".format \
                    (name=str(name),
                     sid=str(media_profile_id))
            print(message)
        else:
            print("[x] ERROR update_media_profile failed since site was not retrieved back successfully")
        # self.test626_test645(name, tenant, False, False, params={"create_site": create_site,
        #                                                          "name": name,
        #                                                          "media_profile_id": media_profile_id,
        #                                                          "media_extension_id": media_extension_id})

    def test003_xpathsitecode(self, name, tenant, create_new=True, **kwargs):
        if create_new:
            create_site, name, media_profile_id, media_extension_id = self.test446(name, tenant)
        else:
            params = kwargs.get("params")
            create_site = params.get("create_site")
            name = params.get("name")
            media_profile_id = params.get("media_profile_id")
            media_extension_id = params.get("media_extension_id")
        site_sid = create_site[0]["links"][0]["href"].split("/")[-1]
        site = self.provisioning.get_single_entry("URL3", site_sid)
        db_id = str(site.get('attributes').get("dbId__l"))

        id_list = []

        def get_customers(response):
            return response['result']['customer']

        customers_list = get_customers(self.common_functions.xpath_query_to_cjp(self.configuration["SITE_XPATH"]))
        for customer in customers_list.get('site'):
            id_list.append(customer['@id'])

        if db_id in id_list:
            message = "[o] Test case (test003_xpathsitecode) {name} XPATH_VALIDATION was successful SITE_ID = {sid}".format \
                (name=str(name),
                 sid=str(site_sid))
        else:
            message = "[x] Test case (test003_xpathsitecode) {name} XPATH_VALIDATION failed SITE_ID = {sid}".format \
                (name=str(name),
                 sid=str(site_sid))
        print(message)

    def combined_test(self, name, tenant, do_not_validate=False):
        create_site, name, media_profile_id, media_extension_id = self.test446(name, tenant, do_not_validate)
        self.test544(name, tenant, create_new=False, params={"create_site": create_site,
                                                             "name": name,
                                                             "media_profile_id": media_profile_id,
                                                             "media_extension_id": media_extension_id})

        self.test561(name, tenant, create_new=False, params={"create_site": create_site,
                                                             "name": name,
                                                             "media_profile_id": media_profile_id,
                                                             "media_extension_id": media_extension_id})
        self.test003_xpathsitecode(name, tenant, create_new=False, params={"create_site": create_site,
                                                                           "name": name,
                                                                           "media_profile_id": media_profile_id,
                                                                           "media_extension_id": media_extension_id})

        self.test626_test645(name, tenant, False, True, params={"create_site": create_site,
                                                                "name": name,
                                                                "media_profile_id": media_profile_id,
                                                                "media_extension_id": media_extension_id})


if __name__ == '__main__':
    test_case = CreateSite()
    test_case.combined_test('TEST4477', '381')
# test_case.test_media_profile_update('TEST4477', '381')
