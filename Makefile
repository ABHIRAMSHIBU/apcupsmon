PREFIX = /usr/bin
SCRIPT = apcupsmon.py
SERVICE = apcupsmond.service
SERVICE_PREFIX = /etc/systemd/system/
install:
	@install $(SCRIPT) $(PREFIX)/apcupsmon
	cp -v $(SERVICE) $(SERVICE_PREFIX)
