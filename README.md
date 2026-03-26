# MACInfo
Get the vendor name by MAC address using a Python script and a database of known vendors
---

**MACInfo** is a CLI program that shows the **vendor name** of a device by its **MAC address**. The program is written in Python and uses a database file (JSON format) with a collection of MAC addresses and information related to them. The database itself is available from the **[maclookup.app](https://maclookup.app/downloads/json-database)** website.

```
$ ./macinfo.py [macaddr]
```

---

**NEW (2026-03-27):** MACInfo now supports database update or download if the database file is missing. The download is automatic if no database file is found when the program is ran with the command `$ ./macinfo.py [macaddr]`. The database update can be performed using the optional argument `--update` or `$ ./macinfo --update`.

