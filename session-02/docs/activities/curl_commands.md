```bash
# We can test aithentication and the POST method
curl --location 'http://myjamjar.com.au/v1/auth/login' --header 'Content-Type: application/json' --header 'Workspaces-Identifier: tenant-pm-001' --header 'X-Integration-Name: Johns-MBP.modem' --data-raw '{"email":"student1@example.com","password":"changeme","workspace_type":"project_management"}'
```

```bash
# We can test the get method.
curl --location 'http://myjamjar.com.au/v1/tasks/projects/01kh05asgt1cq3wx9sd6js6jxk' --header 'Authorization: Bearer 6|FCUM8DSMS32LZcgpexHu2JrFohXClNPmO39R4XOP73593169' --header 'Workspaces-Identifier: tenant-pm-001' --header 'X-Integration-Name: Johns-MBP.modem' --header 'Accept: application/json'
```
