MotorsportReg Credit Creator
============================

Python 3 code to create credits for multiple users across multiple events. The initial reason for creating this concept was that a credit was offered to all leaders of our autocross organization and MSR does not offer - as far as I'm aware - a way to create bulk credits.

Usage
-----

* Copy `inputdata.sample.py` to `inputdata.py`
* Modify all the values in `inputdata.py` to fit your needs
* Set an environment variable `MSR_PASSWORD` to your MSR password (for Bash: `export MSR_PASSWORD='your password'`)
* Invoke `main.py`. Read log output carefully to confirm expected results.

> WARNING: There is no "dry mode" function for this program and the program _will delete_ extra credits that should not exist. Test with small user bases (such as yourself) to ensure the program performs as you wish before applying mass changes.
