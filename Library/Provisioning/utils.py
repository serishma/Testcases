import json
import collections


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Utils:

    def __init__(self, **kwargs):
        self.PRINT = kwargs.get("to_print", False)
        self.message_symbol = {"error": bcolors.FAIL + "[X]" + bcolors.ENDC,
                               "info": bcolors.WARNING + "[i]" + bcolors.ENDC,
                               "ok": bcolors.OKBLUE + "[O]" + bcolors.ENDC}

        self.json_config = self.open_json(file_path=kwargs.get("file_path", None))

    def print_message(self, **kwargs):
        message = kwargs.get("message", None)
        type_ = kwargs.get("type_", "error")
        function = kwargs.get("function")
        if message:
            template = "{symbol} {function} {message}".format(symbol=str(self.message_symbol[type_]),
                                                              function=str(function),
                                                              message=str(message))
            if self.PRINT:
                print(template)

    def open_json(self, **kwargs):
        label = "Utils.open_json"
        file_path = kwargs.get("file_path", None)
        if file_path:
            with open(file_path, 'r') as w:
                file_ = json.loads(w.read())
            return file_
        else:
            self.print_message(message="file_path variable not provided",
                               function=label,
                               type_="error")

    def condition_response(self, **kwargs):
        """
        This function conditions the response to return the analyzer ID
        :param kwargs: argument containing the api response in the following format
                        [ {`links`:
                                    [
                                        {`href`:<url>\analyzerid }
                                    ]
                           }
                         ]
        :return:
        """
        label = "Utils.condition_response"
        data = kwargs.get("data", None)
        if data:
            if type(data) == list:
                data = data[0]
            try:
                link = data["links"][0]
                return link["href"].split("/")[-1]  # this part here return the analyzer ID
            except Exception as e:
                self.print_message(message=str(e),
                                   function=label,
                                   type_="error")
        else:
            self.print_message(message="data variable not provided",
                               function=label,
                               type_="error")
        return None

    def transform_dataframe(self, **kwargs):
        label = "Utils.transform_dataframe"

        def update_nested(obj_, orig_dict, new_dict):
            """
            Recursively merge or update dict-like objects.
                    update_nested({'k1': {'k2': 2}}, {'k1': {'k2': {'k3': 3}}, 'k4': 4})
            result => {'k1': {'k2': {'k3': 3}}, 'k4': 4}
            :param orig_dict: the nested dictionary that needs to be updated
            :param new_dict: the dictionary containing the values that need to be updated in the `orig_dict`

            """
            label_ = "Utils.transform_dataframe->update_nested(inline-function)"
            try:
                for key, val in new_dict.items():
                    if isinstance(val, collections.Mapping):
                        tmp = update_nested(obj_, orig_dict.get(key, {}), val)
                        orig_dict[key] = tmp
                    elif isinstance(val, list):
                        orig_dict[key] = (orig_dict.get(key, []) + val)
                    else:
                        orig_dict[key] = new_dict[key]
            except Exception as error_:
                obj_.print_message(message=str(error_),
                                   function=label_,
                                   type_="error")
                return None
            return orig_dict

        frame = kwargs.get("frame", None)
        as_list = kwargs.get("as_list", True)
        if frame:
            updates = kwargs.get("updates", None)
            if as_list:
                frame = frame[0]
            if updates:
                data = update_nested(self, frame, updates)
                if as_list:
                    data = [data]
                return data
            else:
                self.print_message(message="updates not provided",
                                   function=label,
                                   type_="error")
        else:
            self.print_message(message="frame not provided",
                               function=label,
                               type_="error")
        return None

    def lookup_key(self, **kwargs):
        label = "Utils.lookup_key"

        def nested_lookup(obj_, key, document, wild=False, with_keys=False):
            from six import iteritems
            label_ = "Utils.lookup_key->nested_lookup(inline-function)"
            try:
                if isinstance(document, list):
                    for d in document:
                        for result in nested_lookup(
                                obj_, key, d, wild=wild, with_keys=with_keys
                        ):
                            yield result

                if isinstance(document, dict):
                    for k, v in iteritems(document):
                        if key == k or (wild and key.lower() in k.lower()):
                            if with_keys:
                                yield k, v
                            else:
                                yield v
                        if isinstance(v, dict):
                            for result in nested_lookup(
                                    obj_, key, v, wild=wild, with_keys=with_keys
                            ):
                                yield result
                        elif isinstance(v, list):
                            for d in v:
                                for result in nested_lookup(
                                        obj_, key, d, wild=wild, with_keys=with_keys
                                ):
                                    yield result
            except Exception as error_:
                obj_.print_message(message=str(error_),
                                   function=label_,
                                   type_="error")
                return None

        field = kwargs.get("field", None)
        if field:
            data = kwargs.get("data", None)
            if data:
                return list(nested_lookup(self, field, data))
            else:
                self.print_message(message="data not provided",
                                   function=label,
                                   type_="error")
        else:
            self.print_message(message="field to search not provided",
                               function=label,
                               type_="error")
