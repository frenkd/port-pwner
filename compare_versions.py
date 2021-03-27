EXAMPLE_SSH = '''found 22 open
SSH-2.0-OpenSSH_8.2p1 Ubuntu-4ubuntu0.2'''

EXAMPLE_APACHE = '''found 80 open
HTTP/1.1 400 Bad Request
Date: Sat, 27 Mar 2021 13:48:18 GMT
Server: Apache/2.4.41 (Ubuntu)
Content-Length: 301
Connection: close
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>400 Bad Request</title>
</head><body>
<h1>Bad Request</h1>
<p>Your browser sent a request that this server could not understand.<br />
</p>
<hr>
<address>Apache/2.4.41 (Ubuntu) Server at 127.0.1.1 Port 80</address>
</body></html>'''


def check_output(input_string):
    if input_string is None:
        return None
    if "OpenSSH_" in input_string:
        return "OpenSSH v"+input_string.split("OpenSSH_", 1)[1].split(" ", 1)[0][:3]
    if "Server: Apache/" in input_string:
        return "Apache v"+input_string.split("Server: Apache/", 1)[1].split(" ", 1)[0]
    return None

if __name__ == "__main__":
    parse_output_ssh(EXAMPLE_SSH)
    parse_output_apache(EXAMPLE_APACHE)

