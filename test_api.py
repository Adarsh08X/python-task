try:
    from main import app
    import unittest,json,xlrd

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
        loc = ("testing.xlsx")       
        wb = xlrd.open_workbook(loc)
        sheet = wb.sheet_by_index(0)        
        sheet.cell_value(0, 0)
        s='{'
        for i in range(1,sheet.nrows):
            s+= '"'+str(sheet.cell_value(i,0))+'":"'+str(sheet.cell_value(i,1))+'",'
            print(sheet.cell_value(i, 0))
        s=s[:len(s)-1]+'}'
        info = json.loads(s)

        tester = app.test_client(self)
        response = tester.post("/v1/sanitized/input/", data=json.dumps(info), headers={'Content-Type': 'application/json'})
        statuscode = response.status_code
        self.assertEqual(statuscode,200)
    
    # Test for empty post request
    def test_post_failiure(self):
        tester = app.test_client(self)
        info = {}
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
