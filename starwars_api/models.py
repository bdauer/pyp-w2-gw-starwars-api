from starwars_api.client import SWAPIClient
from starwars_api.exceptions import SWAPIClientError

from test_data import mock_data as json_data  # for debugging

api_client = SWAPIClient()


class BaseModel(object):

    def __init__(self, json_data):
        """
        Dynamically assign all attributes in `json_data` as instance
        attributes of the Model.
        """
        for attribute in json_data:
            setattr(self, attribute, json_data[attribute])
            
        for result in json_data['results']:
            for attribute in result:
                setattr(self, attribute, result[attribute])

    @classmethod
    def get(cls, resource_id):
        """
        Returns an object of current Model requesting data to SWAPI using
        the api_client.
        
        #getattr
        """
        # instantiate person or film
        get_func_name = "get_{0}".format(cls.RESOURCE_NAME)
        get_function = getattr(api_client, get_func_name)
        return get_function(resource_id)

    @classmethod
    def all(cls):
        """
        Returns an iterable QuerySet of current Model. The QuerySet will be
        later in charge of performing requests to SWAPI for each of the
        pages while looping.
        """
        query_set = "{0}QuerySet".format(cls.RESOURCE_NAME.title())


class People(BaseModel):
    """Representing a single person"""
    RESOURCE_NAME = 'people'
    PATH = "http://swapi.co/api/people/"

    def __init__(self, json_data):
        super(People, self).__init__(json_data)
        
        path = self.PATH
        resource_name = self.RESOURCE_NAME

    def __repr__(self):
        return 'Person: {0}'.format(self.name)


class Films(BaseModel):
    RESOURCE_NAME = 'films'

    def __init__(self, json_data):
        super(Films, self).__init__(json_data)

    def __repr__(self):
        return 'Film: {0}'.format(self.title)


class BaseQuerySet(object):

    def __init__(self):
        
        self.objects = []

    def __iter__(self):
        pass

    def __next__(self):
        """
        Must handle requests to next pages in SWAPI when objects in the current
        page were all consumed.
        """
        pass

    next = __next__

    def count(self):
        """
        Returns the total count of objects of current model.
        If the counter is not persisted as a QuerySet instance attr,
        a new request is performed to the API in order to get it.
        """
        pass


class PeopleQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'people'

    def __init__(self):
        super(PeopleQuerySet, self).__init__()

    def __repr__(self):
        return 'PeopleQuerySet: {0} objects'.format(str(len(self.objects)))


class FilmsQuerySet(BaseQuerySet):
    RESOURCE_NAME = 'films'

    def __init__(self):
        super(FilmsQuerySet, self).__init__()

    def __repr__(self):
        return 'FilmsQuerySet: {0} objects'.format(str(len(self.objects)))
