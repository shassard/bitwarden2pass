#!/usr/bin/env python3

import glob
import json
import subprocess


def parseFolders(bitwardenFolders):
    folders = {}
    for folder in bitwardenFolders:
        folders[folder["id"]] = folder["name"]
    return folders


def readBitwardenJson(fname):
    with open(fname) as f:
        inJson = f.read()
        input = json.loads(inJson)
        return input


def insertPass(path, username=None, password="", uris=None, totp=None, extra=None):

    msg = "%s\n" % password
    if username:
        msg += "Username: %s\n" % username
    if uris:
        for uri in uris:
            msg += "URL: %s\n" % uri
    if totp:
        msg += "otpauth://totp/totp-secret?secret=%s\n" % totp
    if extra:
        for name, value in extra:
            msg += "x_%s: %s\n" % (name, value)

    p = subprocess.Popen(["gopass", "insert", "-m", "-f", path], stdin=subprocess.PIPE)
    stdout, stderr = p.communicate(input=msg.encode("utf-8"))
    if p.returncode != 0:
        print("failed %s: %s" % (path, stderr))
    else:
        print("ok %s: %s" % (path, stdout))


def main():

    filename = glob.glob("bitwarden_export_*.json")[0]

    j = readBitwardenJson(filename)

    folders = parseFolders(j["folders"])

    for item in j["items"]:
        path = "%s/%s" % (folders[item["folderId"]], item["name"])
        path = path.replace(" ", "_")
        path = path.replace("_-_", "_")
        path = path.replace("&", "_and_")

        username = None
        password = None
        uris = []
        totp = None
        extra = []

        if "login" in item:
            login = item["login"]
            if "username" in login:
                username = (login["username"],)
            if "password" in login:
                password = (login["password"],)
            if "uris" in login and login["uris"]:
                for uri in login["uris"]:
                    uris.append(uri["uri"])
            if "totp" in login:
                totp = login["totp"]

        if "fields" in item:
            for field in item["fields"]:
                extra.append((field["name"], field["value"]))

        insertPass(
            path,
            username=username,
            password=password,
            uris=uris,
            totp=totp,
            extra=extra,
        )


if __name__ == "__main__":
    main()
