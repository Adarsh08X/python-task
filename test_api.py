try:
    from main import app
    import unittest,json

except Exception as e:
    print("Error: ",e)


class Testing(unittest.TestCase):

    # Testing the base  
    def test_base(self):
        tester = app.test_client(self)
        response = tester.get("/")
        statuscode = response.status_code
        self.assertEqual(statuscode,200)

    # Test for succesfull post request
    def test_post_success(self):
        tester = app.test_client(self)
        info = {"payload": "input1", "payload2": "105 or 1=1"}
        response = tester.post("/v1/sanitized/input/", data=json.dumps(info), headers={'Content-Type': 'application/json'})
        statuscode = response.status_code
        self.assertEqual(statuscode,200)
    
    # Test for empty post request
    def test_post_failiure(self):
        tester = app.test_client(self)
        info = {}
       # print(is_json(str(info)))
        response = tester.post("/v1/sanitized/input/", data=json.dumps(info), headers={'Content-Type': 'application/json'})
        statuscode = response.status_code
        self.assertEqual(statuscode,400)

    # Testing data returned
    def test_result(self):
        tester = app.test_client(self)
        info = {"payload": "input1", "payload2": "105 or 1=1"}
     
        response = tester.post("/v1/sanitized/input/", data=json.dumps(info), headers={'Content-Type': 'application/json'})
        statuscode = response.status_code
        self.assertTrue(b'result' in response.data)


if __name__ == "__main__":
    unittest.main()