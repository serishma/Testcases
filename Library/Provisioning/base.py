import json
import requests
import urllib.parse
# from Library1.Provisioning.utils import Utils
# from Library1.Provisioning.xml_conv import parse
from utils import Utils
from xml_conv import parse


class Base(Utils):
    """
    Base class provides the base methods which contain the CRUD operations.

        POST    -> create_entity :: create a new entity based on the data.
        PUT     -> update_entity :: update entity based on the data provided.
        GET     -> get_entity :: get a single entry.
                -> get_entities :: get all entries.
        DELETE  -> delete_entity :: delete entity based on the ID.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor to the BASE class.

        :param args:
        :param kwargs:
        """
        self.DELAY = 0.5
        super(Base, self).__init__(to_print=True,
                                   file_path='C:/Users/pserishm/Documents/PHC_Automation/TestCases/input.json')

    def create_entity(self, **kwargs):
        """
        POST method binding for creating the entity named `<key>` in the application.
        :param kwargs: arguments to the create entity
                :param url: specifies which URL to use.
                :param data_frame: key that contains frame in json to create the entity.
                :param to_create: dictionary that contains the values to be used.
        :return: json of the created entity / None
        """
        label = "Base.create_entity"
        data_frame = self.json_config.get(kwargs.get("data_frame", None), None)
        if data_frame:
            url = self.json_config.get(kwargs.get("url", None), None)
            if url:
                to_create = kwargs.get("to_create", None)
                if to_create:
                    try:
                        data_frame = self.transform_dataframe(frame=data_frame,
                                                              updates=to_create)
                        response = requests.post(url,
                                                 data=json.dumps(data_frame),
                                                 headers=self.json_config["headers"])
                    except Exception as error_:
                        self.print_message(message=str(error_),
                                           function=label,
                                           type_="error")
                        return None
                    if response.status_code == 200:
                        response = response.json()
                        self.print_message(message="created {entity} => {resp}".format(entity=str(url.split("/")[-1]),
                                                                                       resp=str(response)),
                                           function=label,
                                           type_="ok")
                        return response
                    else:
                        self.print_message(message="<{code}> {entity} => {resp}". \
                                           format(code=str(response.status_code),
                                                  entity=str(url.split("/")[-1]),
                                                  resp=str(response.content)),
                                           function=label,
                                           type_="info")
                        return response.status_code
                else:
                    self.print_message(message="`to_create` config not found in the json else invalid `to_create`",
                                       function=label,
                                       type_="error")
            else:
                self.print_message(message="`url` config not found in the json else invalid `url`",
                                   function=label,
                                   type_="error")

        else:
            self.print_message(message="pass the `data_frame` variable in-order to get the right data frame",
                               function=label,
                               type_="error")
        return None

    def update_entity(self, **kwargs):
        """
        PUT method binding for updating the entity based on the analyser id.
        :param kwargs: arguments to update the entity based on a analyzer id.
                :param url: specifies which URL to use.
                :param data_frame: key that contains frame in json to update the entity.
                :param to_update: dictionary that contains the values to be used.
        :return: json of the created entity / None
        """
        label = "Base.update_entity"
        data_frame = self.json_config.get(kwargs.get("data_frame", None), None)
        if data_frame:
            url = self.json_config.get(kwargs.get("url", None), None)
            if url:
                #url = self.json_config.get(url, None)
                to_update = kwargs.get("to_create", None)
                if to_update:
                    try:
                        data_frame = self.transform_dataframe(frame=data_frame,
                                                              updates=to_update)
                        response = requests.put(url,
                                                data=json.dumps(data_frame),
                                                headers=self.json_config["headers"])
                    except Exception as error_:
                        self.print_message(message=str(error_),
                                           function=label,
                                           type_="error")
                        return None
                    if response.status_code == 200:
                        response = response.json()
                        self.print_message(message="updated {entity} => {resp}".format(entity=str(url.split("/")[-1]),
                                                                                       resp=str(response)),
                                           function=label,
                                           type_="ok")
                        return response
                    else:
                        self.print_message(message="<{code}> {entity} => {resp}". \
                                           format(code=str(response.status_code),
                                                  entity=str(url.split("/")[-1]),
                                                  resp=str(response.content)),
                                           function=label,
                                           type_="info")
                else:
                    self.print_message(message="`to_update` config not found in the json else invalid `to_update`",
                                       function=label,
                                       type_="error")
            else:
                self.print_message(message="`url` config not found in the json else invalid `url`",
                                   function=label,
                                   type_="error")

        else:
            self.print_message(
                message="pass the `data_frame` variable in-order to create the entity with the given data",
                function=label,
                type_="error"
            )

    def get_entity(self, **kwargs):
        """
        GET method binding to get the entity using analyzer ID `<id_>`.
        :param kwargs: arguments to the get entity
                :param url: specifies which URL to use from json file.
                :param id_: analyzer id using which we call the get api.
        :return: json of the created entity / None
        """
        label = "Base.get_entity"
        url = kwargs.get("url", None)
        if url:
            url = self.json_config.get(url, None)
            if url:
                id_ = kwargs.get("id_", None)
                if id_:
                    url = url + "/" + id_
                    try:
                        response = requests.get(url,
                                                headers=self.json_config["headers"])
                    except Exception as error_:
                        self.print_message(message=str(error_),
                                           function=label,
                                           type_="error")
                        return None
                    if response.status_code == 200:
                        response = response.json()
                        self.print_message(message="fetched {entity} => {resp}".format(entity=str(url.split("/")[-1]),
                                                                                       resp=str(response)),
                                           function=label,
                                           type_="ok")
                        return response
                    else:
                        self.print_message(message="<{code}> {entity} => {resp}". \
                                           format(code=str(response.status_code),
                                                  entity=str(url.split("/")[-1]),
                                                  resp=str(response.content)),
                                           function=label,
                                           type_="info")
                else:
                    self.print_message(
                        message="pass the `id_` variable in-order to get the entity using the analyzer ID",
                        function=label,
                        type_="error"
                    )
            else:
                self.print_message(message="`url` config not found in the json else invalid `url`",
                                   function=label,
                                   type_="error")

        else:
            self.print_message(message="pass the `url` variable in-order to access the right URL",
                               function=label,
                               type_="error")
        return None

    def get_entities(self, **kwargs):
        """
        GET method binding to get the all entities.
        :param kwargs: arguments to the get entity
                :param url: specifies which URL to use from json file.
        :return: json of the created entity / None
        """
        label = "Base.get_entities"
        url = kwargs.get("url", None)
        if url:
            url = self.json_config.get(url, None)
            if url:
                response = requests.get(url,
                                        headers=self.json_config["headers"])
                if response.status_code == 200:
                    response = response.json()
                    self.print_message(message="fetched {entity} => {resp}".format(entity=str(url.split("/")[-1]),
                                                                                   resp=str(response)),
                                       function=label,
                                       type_="ok")
                    filter_ = kwargs.get("filter_", None)
                    if filter_:
                        response = self.lookup_key(field=filter_, data=response)
                    return response
                else:
                    self.print_message(message="<{code}> {entity} => {resp}". \
                                       format(code=str(response.status_code),
                                              entity=str(url.split("/")[-1]),
                                              resp=str(response.content)),
                                       function=label,
                                       type_="info")
            else:
                self.print_message(message="`url` config not found in the json else invalid `url`",
                                   function=label,
                                   type_="error")

        else:
            self.print_message(message="pass the `url` variable in-order to access the right URL",
                               function=label,
                               type_="error")

    def delete_entity(self, **kwargs):
        """
        DELETE method binding for deleting the entity using analyzer ID `<id_>`.
        :param kwargs: arguments to the delete entity
                :param url: specifies which URL to use from json file.
                :param id_: analyzer id using which we call the delete api.
        :return: json of the created entity / None
        """
        label = "Base.delete_entity"
        url = kwargs.get("url", None)
        if url:
            url = self.json_config.get(url, None)
            if url:
                id_ = kwargs.get("id_", None)
                if id_:
                    url = url + "/" + id_
                    try:
                        response = requests.delete(url,
                                                   headers=self.json_config["headers"])
                    except Exception as error_:
                        self.print_message(message=str(error_),
                                           function=label,
                                           type_="error")
                        return None
                    if response.status_code == 200:
                        response = response.json()
                        self.print_message(message="deleted {entity} => {resp}".format(entity=str(url.split("/")[-1]),
                                                                                       resp=str(response)),
                                           function=label,
                                           type_="ok")
                        return response
                    else:
                        self.print_message(message="<{code}> {entity} => {resp}". \
                                           format(code=str(response.status_code),
                                                  entity=str(url.split("/")[-1]),
                                                  resp=str(response.content)),
                                           function=label,
                                           type_="info")
                else:
                    self.print_message(
                        message="pass the `id_` variable in-order to delete the entity using the analyzer ID",
                        function=label,
                        type_="error"
                    )
            else:
                self.print_message(message="`url` config not found in the json else invalid `url`",
                                   function=label,
                                   type_="error")

        else:
            self.print_message(message="pass the `url` variable in-order to access the right URL",
                               function=label,
                               type_="error")
        return None

    def xpath_query(self, **kwargs):
        """
        XPATH method to get the xpath data from the api call.
        :param kwargs: arguments to the delete entity
                :param xpath: specifies which XPATH to use from json file
                :param attribute: attributes specified for the above xpath..
        :return: list of all xpath entites / None
        """
        label = "Base.xpath_query"
        xpath = kwargs.get("xpath", None)
        attribute = kwargs.get("attribute", "*")

        if xpath:

            def urlencode(obj_, xpath):
                label_ = "Base.xpath_query->urlencode(inline-function)"
                try:
                    return urllib.parse.quote_plus(xpath)
                except Exception as error_:
                    obj_.print_message(message=str(error_),
                                       function=label_,
                                       type_="error")
                return None

            def get_data(obj_, xpath, attribute):
                label_ = "Base.xpath_query->get_data(inline-function)"
                url = "http://ace103.dev.broadcloudcc.com:9180/xpaths/DispatchServlet?xpath=" + \
                      urlencode(obj_, xpath) + \
                      "&attributes={attr}&Query=++++++Query++++++".format(attr=str(attribute))
                try:
                    response = requests.get(url)
                    if response.status_code == 200:
                        try:
                            return parse(response.text)
                        except Exception as error_:
                            obj_.print_message(message=str(error_),
                                               function=label_,
                                               type_="error")
                    else:
                        obj_.print_message(message="<{code}> {entity} => {resp}". \
                                           format(code=str(response.status_code),
                                                  entity=str("xpath"),
                                                  resp=str(response.content)),
                                           function=label_,
                                           type_="info")
                        return None
                except Exception as error_:
                    obj_.print_message(message=str(error_),
                                       function=label_,
                                       type_="error")
                    return None

                return response

            return get_data(self, xpath, attribute)
        else:
            self.print_message(message="pass the `xpath` variable in-order to access the right XPATH",
                               function=label,
                               type_="error")
        return None

    def validate_xml(self, **kwargs):
        """
        XML validate method to validate the xml data vs the created entity.
        :param kwargs: arguments to the delete entity
                :param xpath: specifies which XPATH to use from json file.
                :param id_: analyzer id of the specific entity.
                :param url_key: specifies which URL to use from json file.
                :param attribute: attribute passed along with the XPATH. (optional)
                :param api_lookup: lookup key for the api data. (optional)
                :param xml_lookup: lookup key for the xml data. (optional)
        :return: list of all xpath entites / None
        """
        label = "Base.validate"

        def frame_reduce(obj_, field, data):
            label_ = "Base.validate->frame_reduce(inline-function)"

            try:
                return self.lookup_key(field=field, data=data)
            except Exception as error_:
                obj_.print_message(message=str(error_),
                                   function=label_,
                                   type_="error")

        xpath = kwargs.get("xpath", None)
        if xpath:
            xpath = self.json_config.get(xpath, None)
            if xpath:
                id_ = kwargs.get("id_", None)
                if id_:
                    url_key = kwargs.get("url_key", None)
                    if url_key:
                        attribute = kwargs.get("attribute", "*")
                        field = kwargs.get("field", self.json_config.get(url_key).split("/")[-1])
                        api_lookup = kwargs.get("api_lookup", "dbId__l")
                        xml_lookup = kwargs.get("xml_lookup", "@id")
                        xml_data = self.xpath_query(xpath=xpath, attribute=attribute)
                        xml_data = frame_reduce(self, field=field, data=xml_data)
                        if xml_data:
                            entity = self.get_entity(url=url_key,
                                                     id_=id_)
                            if entity:
                                database_id = self.lookup_key(field=api_lookup,
                                                              data=entity)
                                if database_id:
                                    if type(database_id) == list:
                                        database_id = str(database_id[0])
                                    else:
                                        database_id = str(database_id)
                                    id_xml = self.lookup_key(field=xml_lookup,
                                                              data=xml_data)
                                    if database_id in id_xml:
                                        return True
                                else:
                                    self.print_message(
                                        message="{field} not found in data => {resp}".format(field=str(api_lookup),
                                                                                             resp=str(database_id)),
                                        function=label,
                                        type_="error")

                            else:
                                self.print_message(
                                    message="get_entity return invalid or null",
                                    function=label,
                                    type_="error")
                        else:
                            self.print_message(message="`xml_data` was => {data}".format(data=str(xml_data)),
                                               function=label,
                                               type_="error")
                    else:
                        self.print_message(message="pass the `url_key` variable in-order to access the right URL",
                                           function=label,
                                           type_="error")
                else:
                    self.print_message(message="please pass a valid ID to verify against",
                                       function=label,
                                       type_="error")
            else:
                self.print_message(message="{key} config not found in the json else invalid `xpath`". \
                                   format(key=str(xpath)),
                                   function=label,
                                   type_="error")
        else:
            self.print_message(message="pass the `xpath` variable in-order to access the right XPATH",
                               function=label,
                               type_="error")
        return False
