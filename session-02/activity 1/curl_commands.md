```bash
# We can test aithentication and the POST method
curl --location 'https://myjamjar.com.au/v1/auth/login' --header 'Content-Type: application/json' --header 'Workspaces-Identifier: tenant-pm-001' --header 'X-Integration-Name: Johns-MBP.modem' --json '{"email":"student1@example.com","password":"changeme","workspace_type":"project_management"}'
```

```bash
# We can test the get method use the token from the command above
curl --location 'https://myjamjar.com.au/v1/projects' --header 'Authorization: Bearer 152|FArVmLuMxdp7DpSa0H97cI57Dj1nMmCl9ySoozZtc694906d' --header 'Workspaces-Identifier: tenant-pm-026' --header 'X-Integration-Name: Johns-MBP.modem' --header 'Accept: application/json'
```
