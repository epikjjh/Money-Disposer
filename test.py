import unittest
import requests
import subprocess
import json
import sqlite3


class APITest(unittest.TestCase):
    def setUp(self):
        self.url = "http://127.0.0.1:8080/disposer"
        # Dictionary: {Token: (X-USER-ID, X-ROOM-ID)}
        self.tokens = {}
        # run server
        subprocess.run(["bash", "run.sh"])

    def tearDown(self):
        # Search for port 8080's pid to shutdown api server
        netstat = subprocess.Popen(
            ["netstat", "-ntlp"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        grep = subprocess.Popen(
            ["grep", "8080"], stdin=netstat.stdout, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        netstat.stdout.close()
        res, err = grep.communicate()
        res = res.decode('utf-8').split()[-1].split('/')[0]
        # Kill pid
        subprocess.run(["kill", res])

        # Delete all data
        conn = sqlite3.connect('disposer/db.sqlite3')
        sql = "delete from apiServer_ticket"
        cur = conn.cursor()
        cur.execute(sql)
        sql = "delete from apiServer_userlist"
        cur.execute(sql)
        conn.commit()

    def test_spread(self):
        for i in range(50):
            headers = {"Content-Type": "application/json; charset=utf-8",
                       "X-ROOM-ID": str(i), "X-USER-ID": str(i)}
            data = {'num': str(i), 'amount': str(50-i)}
            res = requests.post(self.url, headers=headers,
                                data=json.dumps(data))
            self.assertIn("application/json", res.headers["Content-Type"])
            self.assertEqual(res.status_code, 200)

            ret = res.json()
            self.tokens[ret["token"]] = (str(i), str(i))

    def test_receive(self):
        pass

    def test_retrieve(self):
        pass


if __name__ == "__main__":
    unittest.main()
