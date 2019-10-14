# bitwarden2pass
bitwarden json to password-store converter

This is a super simple bitwarden json export to password-store converter.

We're expecting that you're using [gopass](https://github.com/gopasspw/gopass) for processing the new records. It's trivial to replace the **gopass** argument to Popen with **pass** in the case that you're using the regular old password-store executable.
