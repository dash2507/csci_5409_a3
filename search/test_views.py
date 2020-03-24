from app import app
import os
import unittest


class BasicTests(unittest.TestCase):

    ############################
    #### setup and teardown ####
    ############################

    # executed prior to each test
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # executed after each test
    def tearDown(self):
        pass


###############
#### tests ####
###############


    def test_main_page(self):
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)

    def test_search(self):
        response = self.app.get(
            '/search', query_string=dict(query='The Apostolic Tradition of Hippolytus'))
        self.assertEqual(response.status_code, 200)

    def test_notes(self):
        response = self.app.get(
            '/notes', query_string=dict(keyword='The Apostolic Tradition of Hippolytus'))
        self.assertEqual(response.status_code, 200)

    def test_add_note(self):
        response = self.app.get('/add_note', query_string=dict(
            keyword='The Apostolic Tradition of Hippolytus', note='This is Sample Note.'))
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
