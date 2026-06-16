import asyncio
import socket
from typing import Optional


class PortScanner:
    def __init__(self):
        self.common_ports = [
            21, 22, 23, 25, 53, 80, 81, 110, 111, 123, 137, 139, 143, 161, 179, 389,
            443, 445, 465, 500, 514, 543, 587, 593, 636, 646, 873, 990, 993, 995,
            1025, 1026, 1027, 1028, 1029, 1080, 1194, 1352, 1433, 1434, 1521, 2049,
            2082, 2083, 2086, 2087, 2095, 2096, 2100, 2222, 2301, 2381, 2443, 2483,
            2484, 2745, 2967, 3000, 3001, 3128, 3306, 3310, 3389, 3390, 3500, 3541,
            3632, 3690, 3900, 3984, 4000, 4001, 4002, 4040, 4045, 4224, 4243, 4321,
            4333, 4443, 4444, 4500, 4567, 4662, 4848, 4899, 5000, 5001, 5003, 5004,
            5005, 5050, 5051, 5060, 5061, 5100, 5120, 5222, 5223, 5250, 5351, 5353,
            5357, 5432, 5445, 5480, 5481, 5554, 5555, 5560, 5631, 5632, 5666, 5667,
            5672, 5678, 5683, 5724, 5800, 5801, 5802, 5810, 5811, 5900, 5901, 5902,
            5903, 5984, 5985, 5986, 6000, 6001, 6002, 6003, 6082, 6379, 6380, 6443,
            6444, 6514, 6566, 6580, 6660, 6661, 6662, 6663, 6664, 6665, 6666, 6667,
            6668, 6669, 6679, 6697, 6701, 6881, 6891, 6901, 6969, 7000, 7001, 7002,
            7003, 7004, 7005, 7006, 7007, 7008, 7009, 7010, 7020, 7021, 7022, 7023,
            7024, 7025, 7050, 7070, 7071, 7080, 7090, 7100, 7110, 7120, 7144, 7171,
            7200, 7201, 7300, 7301, 7312, 7396, 7420, 7443, 7496, 7510, 7547, 7548,
            7674, 7675, 7676, 7741, 7777, 7778, 7779, 7800, 7801, 7802, 7831, 7878,
            7879, 7880, 7881, 7890, 7900, 7911, 7920, 7921, 7999, 8000, 8001, 8002,
            8003, 8004, 8005, 8006, 8007, 8008, 8009, 8010, 8011, 8020, 8021, 8022,
            8031, 8042, 8043, 8045, 8050, 8060, 8069, 8070, 8080, 8081, 8082, 8083,
            8084, 8085, 8086, 8087, 8088, 8089, 8090, 8091, 8092, 8093, 8095, 8096,
            8097, 8098, 8099, 8100, 8101, 8112, 8118, 8123, 8139, 8140, 8161, 8172,
            8181, 8191, 8192, 8193, 8194, 8200, 8222, 8243, 8244, 8266, 8280, 8290,
            8291, 8300, 8332, 8333, 8384, 8385, 8400, 8403, 8443, 8444, 8500, 8520,
            8521, 8543, 8544, 8554, 8560, 8600, 8649, 8651, 8652, 8654, 8675, 8686,
            8732, 8733, 8743, 8744, 8750, 8760, 8761, 8763, 8764, 8765, 8766, 8770,
            8778, 8779, 8780, 8786, 8787, 8788, 8790, 8800, 8811, 8820, 8834, 8835,
            8840, 8843, 8844, 8850, 8860, 8873, 8875, 8878, 8879, 8880, 8881, 8882,
            8883, 8884, 8885, 8886, 8887, 8888, 8889, 8890, 8891, 8892, 8899, 8900,
            8910, 8911, 8920, 8930, 8945, 8954, 8965, 8980, 8981, 8983, 8989, 8990,
            8991, 8994, 8995, 8997, 8998, 8999, 9000, 9001, 9002, 9003, 9004, 9005,
            9006, 9007, 9008, 9009, 9010, 9011, 9020, 9021, 9040, 9042, 9043, 9045,
            9050, 9051, 9060, 9071, 9080, 9081, 9084, 9085, 9086, 9087, 9088, 9090,
            9091, 9092, 9093, 9094, 9095, 9096, 9097, 9098, 9099, 9100, 9101, 9102,
            9103, 9105, 9106, 9107, 9110, 9111, 9120, 9150, 9151, 9152, 9160, 9170,
            9180, 9191, 9200, 9210, 9220, 9222, 9229, 9230, 9240, 9250, 9260, 9270,
            9271, 9277, 9278, 9280, 9283, 9284, 9285, 9287, 9290, 9293, 9294, 9295,
            9300, 9301, 9306, 9310, 9312, 9318, 9320, 9332, 9333, 9340, 9343, 9344,
            9345, 9346, 9370, 9371, 9372, 9380, 9382, 9387, 9389, 9390, 9392, 9393,
            9394, 9395, 9396, 9397, 9400, 9401, 9402, 9403, 9409, 9415, 9418, 9443,
            9444, 9450, 9460, 9485, 9486, 9490, 9491, 9495, 9500, 9502, 9503, 9504,
            9505, 9506, 9510, 9520, 9530, 9535, 9540, 9550, 9559, 9560, 9561, 9593,
            9594, 9595, 9596, 9597, 9600, 9610, 9612, 9614, 9616, 9618, 9620, 9622,
            9625, 9626, 9627, 9628, 9629, 9630, 9631, 9632, 9666, 9670, 9671, 9672,
            9673, 9675, 9676, 9677, 9678, 9679, 9680, 9690, 9695, 9700, 9701, 9710,
            9711, 9720, 9721, 9722, 9723, 9728, 9729, 9730, 9731, 9732, 9735, 9736,
            9747, 9750, 9751, 9753, 9760, 9761, 9762, 9770, 9771, 9772, 9773, 9774,
            9775, 9776, 9780, 9781, 9782, 9783, 9784, 9785, 9786, 9787, 9788, 9789,
            9790, 9791, 9792, 9793, 9794, 9795, 9796, 9797, 9798, 9799, 9800,
            9876, 9877, 9878, 9888, 9898, 9900, 9917, 9929, 9943, 9944, 9968, 9981,
            9987, 9990, 9991, 9992, 9993, 9994, 9995, 9996, 9997, 9998, 9999,
            10000, 10001, 10002, 10003, 10004, 10005, 10006, 10007, 10008, 10009,
            10010, 10011, 10012, 10050, 10080, 10110, 10113, 10114, 10115, 10116,
            10125, 10161, 10162, 10200, 10201, 10202, 10203, 10204, 10205, 10206,
            10333, 10389, 10443, 10505, 10514, 10778, 10800, 10805, 10809, 10810,
            10880, 10990, 11000, 11110, 11111, 11211, 11300, 11301, 11302, 11371,
            11433, 11508, 11720, 11967, 12000, 12174, 12265, 12321, 12322, 12345,
            12346, 12443, 12489, 12701, 12777, 13000, 13008, 13080, 13131, 13291,
            13337, 13364, 13365, 13444, 13456, 13457, 13579, 13722, 13782, 13783,
            14000, 14001, 14141, 14142, 14143, 14238, 14250, 14441, 14442, 14443,
            14500, 14533, 14534, 14652, 15000, 15002, 15003, 15004, 15118, 15151,
            15201, 15202, 15203, 15283, 15345, 15363, 15555, 15556, 15660, 15672,
            15742, 16010, 16012, 16016, 16080, 16113, 16161, 16200, 16250,
            16300, 16301, 16310, 16311, 16360, 16361, 16370, 16378, 16379,
            16380, 16384, 16400, 16401, 16402, 16403, 16410, 16413, 16420,
            16430, 16440, 16450, 16500, 16510, 16520, 16600, 16660, 16680,
            16700, 16710, 16711, 16800, 16850, 16860, 16870, 16880, 16890,
            16900, 16950, 16992, 16993, 17000, 17100, 17101, 17102, 17103,
            17104, 17105, 17106, 17107, 17108, 17109, 17110, 17120, 17130,
            17200, 17210, 17220, 17230, 17240, 17250, 17300, 17310, 17320,
            17400, 17410, 17420, 17430, 17500, 17600, 17700, 17777, 17778,
            17800, 17810, 17820, 17830, 17900, 17950, 17988, 17990, 18000,
            18080, 18081, 18082, 18090, 18091, 18092, 18100, 18101, 18102,
            18103, 18104, 18110, 18111, 18112, 18113, 18114, 18180, 18181,
            18200, 18210, 18220, 18221, 18250, 18251, 18260, 18300, 18310,
            18330, 18331, 18332, 18333, 18334, 18335, 18400, 18444, 18500,
            18600, 18605, 18700, 18750, 18769, 18800, 18801, 18802, 18803,
            18810, 18811, 18812, 18820, 18821, 18830, 18831, 18832, 18835,
            18840, 18850, 18880, 18881, 18882, 18883, 18884, 18885, 18886,
            18887, 18888, 18900, 18901, 18910, 18920, 19000, 19001, 19010,
            19020, 19080, 19081, 19090, 19100, 19101, 19102, 19103, 19104,
            19105, 19106, 19107, 19108, 19109, 19110, 19130, 19140, 19150,
            19200, 19220, 19250, 19283, 19294, 19300, 19302, 19305, 19315,
            19350, 19400, 19410, 19412, 19415, 19500, 19501, 19510, 19600,
            19601, 19610, 19620, 19630, 19638, 19640, 19700, 19710, 19771,
            19772, 19800, 19801, 19810, 19842, 19850, 19900, 19910, 19920,
            19930, 19940, 19950, 19960, 19970, 19980, 19990, 20000,
        ]
        self.service_map = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
            80: "HTTP", 110: "POP3", 111: "RPC", 123: "NTP", 137: "NetBIOS",
            139: "NetBIOS", 143: "IMAP", 161: "SNMP", 389: "LDAP", 443: "HTTPS",
            445: "SMB", 465: "SMTPS", 500: "IKE", 514: "Syslog", 543: "LDAP",
            587: "SMTP", 593: "HTTP RPC", 636: "LDAPS", 873: "RSYNC",
            990: "FTPS", 992: "TelnetS", 993: "IMAPS", 995: "POP3S",
            1080: "SOCKS", 1194: "OpenVPN", 1433: "MSSQL", 1521: "Oracle DB",
            2049: "NFS", 2082: "cPanel", 2083: "cPanel SSL", 2222: "DirectAdmin",
            2375: "Docker", 2376: "Docker TLS", 2483: "Oracle DB", 2484: "Oracle DB SSL",
            3000: "Grafana/Node", 3128: "Squid", 3306: "MySQL", 3389: "RDP",
            4000: "Node.js", 4001: "Node.js SSL", 4040: "Yearch", 4224: "CDP",
            4243: "Docker", 4444: "Metasploit", 4560: "Logstash", 4567: "Sinatra",
            4848: "GlassFish", 4899: "Radmin", 5000: "Flask/Upnp", 5001: "Synology",
            5040: "DDI", 5060: "SIP", 5061: "SIP TLS", 5141: "AOL", 5222: "XMPP",
            5223: "XMPP SSL", 5269: "XMPP Server", 5342: "Kazaa", 5351: "NAT-PMP",
            5353: "mDNS", 5432: "PostgreSQL", 5554: "Sasser", 5555: "Android ADB",
            5601: "Kibana", 5631: "pcAnywhere", 5666: "NRPE", 5672: "RabbitMQ",
            5800: "VNC", 5810: "VNC", 5900: "VNC", 5901: "VNC", 5984: "CouchDB",
            5985: "WinRM", 5986: "WinRM SSL", 6000: "X11", 6001: "X11",
            6379: "Redis", 6380: "Redis SSL", 6443: "Kubernetes", 6514: "Syslog TLS",
            6566: "SANE", 6580: "Parsec", 6660: "IRC", 6661: "IRC", 6662: "IRC",
            6663: "IRC", 6664: "IRC", 6665: "IRC", 6666: "IRC", 6667: "IRC",
            6668: "IRC", 6669: "IRC", 6679: "IRC SSL", 6697: "IRC SSL",
            7001: "WebLogic", 7002: "WebLogic SSL", 7070: "RealServer",
            7071: "Zimbra", 7077: "Jenkins", 7171: "Scorched 3D",
            7200: "DDS", 7210: "MaxDB", 7274: "VibeStreamer",
            7396: "Folding@home", 7443: "Oracle HTTPS", 7457: "WU-2",
            7474: "Neo4j", 7475: "Neo4j SSL", 7481: "Openfire",
            7547: "CWMP", 7574: "DCS", 7575: "DCS", 7626: "Poco",
            7654: "JetDirect", 7674: "iTunes", 7675: "iTunes", 7676: "iTunes",
            7717: "KMS", 7741: "Game", 7777: "Game", 7778: "Game", 7779: "Game",
            7800: "ASAP", 7810: "ASAP", 7845: "APC", 7846: "APC",
            7878: "Game", 7887: "Game", 7900: "Game", 7901: "Game", 7902: "Game",
            7911: "Nessus", 7912: "Nessus", 7913: "Nessus",
            8000: "HTTP Alt", 8001: "HTTP Alt", 8002: "HTTP Alt",
            8008: "HTTP Alt", 8009: "AJP", 8010: "XMPP File",
            8020: "HTTP Alt", 8030: "HTTP Alt", 8042: "HTTP Alt",
            8060: "HTTP Alt", 8061: "HTTP Alt", 8069: "Odoo",
            8070: "HTTP Alt", 8080: "HTTP Proxy", 8081: "HTTP Alt",
            8082: "HTTP Alt", 8083: "HTTP Alt", 8084: "HTTP Alt",
            8085: "HTTP Alt", 8086: "InfluxDB", 8087: "HTTP Alt",
            8088: "HTTP Alt", 8089: "Splunk", 8090: "HTTP Alt",
            8091: "Couchbase", 8092: "Couchbase", 8096: "Emby/Jellyfin",
            8100: "HTTP Alt", 8111: "Skype", 8112: "PAC", 8118: "Privoxy",
            8123: "Polipo", 8139: "Puppet", 8140: "Puppet SSL",
            8161: "ActiveMQ", 8172: "MS Deploy", 8181: "HTTP Alt",
            8200: "HTTP Alt", 8222: "VMware", 8243: "HTTPS Alt",
            8280: "HTTP Alt", 8291: "Winbox", 8300: "HTTP Alt",
            8332: "Bitcoin", 8333: "Bitcoin", 8334: "Bitcoin",
            8384: "Syncthing", 8400: "HTTP Alt", 8403: "Comodo",
            8443: "HTTPS Alt", 8500: "HTTP Alt", 8530: "WSUS",
            8531: "WSUS SSL", 8580: "HTTP Alt", 8649: "Ganglia",
            8668: "AirPlay", 8686: "JMX", 8732: "HTTP Alt",
            8743: "HTTP Alt", 8750: "HTTP Alt", 8760: "HTTP Alt",
            8761: "Eureka", 8765: "HTTP Alt", 8770: "HTTP Alt",
            8778: "HTTP Alt", 8787: "HTTP Alt", 8790: "HTTP Alt",
            8800: "HTTP Alt", 8811: "HTTP Alt", 8820: "HTTP Alt",
            8834: "Nessus", 8840: "HTTP Alt", 8843: "HTTPS Alt",
            8850: "HTTP Alt", 8860: "HTTP Alt", 8873: "HTTP Alt",
            8875: "HTTP Alt", 8880: "HTTP Alt", 8881: "HTTP Alt",
            8882: "HTTP Alt", 8883: "MQTT", 8884: "HTTP Alt",
            8887: "HTTP Alt", 8888: "HTTP Alt", 8889: "HTTP Alt",
            8890: "HTTP Alt", 8891: "HTTP Alt", 8892: "HTTP Alt",
            8899: "cPanel", 8900: "HTTP Alt", 8910: "HTTP Alt",
            8980: "HTTP Alt", 8983: "Solr", 8990: "HTTP Alt",
            8991: "HTTP Alt", 8997: "HTTP Alt", 8998: "HTTP Alt",
            8999: "HTTP Alt", 9000: "SonarQube", 9001: "HTTP Alt",
            9002: "HTTP Alt", 9003: "HTTP Alt", 9004: "HTTP Alt",
            9005: "HTTP Alt", 9006: "HTTP Alt", 9007: "HTTP Alt",
            9008: "HTTP Alt", 9009: "HTTP Alt", 9010: "HTTP Alt",
            9020: "HTTP Alt", 9025: "HTTP Alt", 9030: "HTTP Alt",
            9042: "Cassandra", 9043: "WebSphere", 9050: "HTTP Alt",
            9060: "WebSphere", 9080: "HTTP Alt", 9081: "HTTP Alt",
            9090: "HTTP Alt", 9091: "HTTP Alt", 9092: "Kafka",
            9093: "Kafka SSL", 9094: "Kafka", 9095: "HTTP Alt",
            9096: "HTTP Alt", 9097: "HTTP Alt", 9098: "HTTP Alt",
            9099: "HTTP Alt", 9100: "Printer", 9101: "HTTP Alt",
            9102: "HTTP Alt", 9103: "HTTP Alt", 9110: "HTTP Alt",
            9111: "HTTP Alt", 9120: "HTTP Alt", 9150: "HTTP Alt",
            9151: "HTTP Alt", 9160: "HTTP Alt", 9191: "HTTP Alt",
            9200: "Elasticsearch", 9210: "HTTP Alt", 9220: "HTTP Alt",
            9229: "Node Debug", 9295: "HTTP Alt", 9300: "Elasticsearch",
            9312: "Sphinx", 9320: "HTTP Alt", 9343: "HTTP Alt",
            9350: "HTTP Alt", 9351: "HTTP Alt", 9352: "HTTP Alt",
            9353: "HTTP Alt", 9354: "HTTP Alt", 9355: "HTTP Alt",
            9356: "HTTP Alt", 9357: "HTTP Alt", 9358: "HTTP Alt",
            9359: "HTTP Alt", 9360: "HTTP Alt", 9361: "HTTP Alt",
            9362: "HTTP Alt", 9363: "HTTP Alt", 9370: "HTTP Alt",
            9380: "HTTP Alt", 9390: "HTTP Alt", 9400: "HTTP Alt",
            9415: "HTTP Alt", 9418: "Git", 9443: "HTTPS Alt",
            9500: "HTTP Alt", 9530: "HTTP Alt", 9535: "HTTP Alt",
            9593: "HTTP Alt", 9594: "HTTP Alt", 9595: "HTTP Alt",
            9596: "HTTP Alt", 9597: "HTTP Alt", 9600: "HTTP Alt",
            9876: "HTTP Alt", 9898: "HTTP Alt", 9900: "HTTP Alt",
            9981: "HTTP Alt", 9987: "HTTP Alt", 9990: "HTTP Alt",
            9991: "HTTP Alt", 9992: "HTTP Alt", 9993: "HTTP Alt",
            9994: "HTTP Alt", 9995: "HTTP Alt", 9996: "HTTP Alt",
            9997: "Splunk", 9998: "HTTP Alt", 9999: "HTTP Alt",
            10000: "Webmin", 10001: "HTTP Alt", 10009: "HTTP Alt",
            10010: "HTTP Alt", 10050: "Zabbix", 10051: "Zabbix",
            10134: "HTTP Alt", 10161: "SNMP", 10162: "SNMP",
            10200: "HTTP Alt", 10250: "Kubelet", 10255: "Kubelet",
            10333: "HTTP Alt", 10389: "HTTP Alt", 10443: "HTTPS Alt",
            10500: "HTTP Alt", 10505: "HTTP Alt", 10514: "Syslog",
            10600: "HTTP Alt", 10601: "HTTP Alt", 10700: "HTTP Alt",
            10800: "HTTP Alt", 10809: "HTTP Alt", 10990: "HTTP Alt",
            11000: "HTTP Alt", 11110: "HTTP Alt", 11111: "HTTP Alt",
            11211: "Memcached", 11300: "HTTP Alt", 11301: "HTTP Alt",
            11371: "OpenPGP", 11433: "HTTP Alt", 11434: "Ollama",
            11508: "HTTP Alt", 11720: "HTTP Alt", 12000: "HTTP Alt",
            12174: "HTTP Alt", 12200: "HTTP Alt", 12321: "HTTP Alt",
            12345: "NetBus", 12443: "HTTPS Alt", 12489: "HTTP Alt",
            12999: "HTTP Alt", 13000: "HTTP Alt", 13008: "HTTP Alt",
            13080: "HTTP Alt", 13131: "HTTP Alt", 13291: "HTTP Alt",
            13337: "HTTP Alt", 13364: "HTTP Alt", 13365: "HTTP Alt",
            13444: "HTTP Alt", 13579: "HTTP Alt", 13722: "HTTP Alt",
            13782: "HTTP Alt", 13783: "HTTP Alt", 14000: "HTTP Alt",
            14141: "HTTP Alt", 14142: "HTTP Alt", 14143: "HTTP Alt",
            14238: "HTTP Alt", 14250: "HTTP Alt", 14441: "HTTP Alt",
            14442: "HTTP Alt", 14443: "HTTP Alt", 14500: "HTTP Alt",
            14652: "HTTP Alt", 15000: "HTTP Alt", 15002: "HTTP Alt",
            15118: "HTTP Alt", 15151: "HTTP Alt", 15345: "HTTP Alt",
            15363: "HTTP Alt", 15555: "HTTP Alt", 15660: "HTTP Alt",
            15672: "RabbitMQ", 15742: "HTTP Alt", 16010: "HTTP Alt",
            16012: "HTTP Alt", 16016: "HTTP Alt", 16080: "HTTP Alt",
            16113: "HTTP Alt", 16161: "HTTP Alt", 16200: "HTTP Alt",
            16250: "HTTP Alt", 16300: "HTTP Alt", 16310: "HTTP Alt",
            16379: "HTTP Alt", 16384: "HTTP Alt", 16400: "HTTP Alt",
            16413: "HTTP Alt", 16500: "HTTP Alt", 16600: "HTTP Alt",
            16660: "HTTP Alt", 16680: "HTTP Alt", 16700: "HTTP Alt",
            16800: "HTTP Alt", 16850: "HTTP Alt", 16860: "HTTP Alt",
            16880: "HTTP Alt", 16890: "HTTP Alt", 16900: "HTTP Alt",
            16950: "HTTP Alt", 16992: "HTTP Alt", 16993: "HTTP Alt",
            17000: "HTTP Alt", 17100: "HTTP Alt", 17101: "HTTP Alt",
            17200: "HTTP Alt", 17250: "HTTP Alt", 17300: "HTTP Alt",
            17400: "HTTP Alt", 17500: "HTTP Alt", 17600: "HTTP Alt",
            17700: "HTTP Alt", 17777: "HTTP Alt", 17800: "HTTP Alt",
            17900: "HTTP Alt", 17950: "HTTP Alt", 17988: "HTTP Alt",
            17990: "HTTP Alt", 18000: "HTTP Alt", 18080: "HTTP Alt",
            18081: "HTTP Alt", 18082: "HTTP Alt", 18090: "HTTP Alt",
            18100: "HTTP Alt", 18101: "HTTP Alt", 18110: "HTTP Alt",
            18180: "HTTP Alt", 18200: "HTTP Alt", 18210: "HTTP Alt",
            18250: "HTTP Alt", 18251: "HTTP Alt", 18300: "HTTP Alt",
            18330: "HTTP Alt", 18331: "HTTP Alt", 18332: "HTTP Alt",
            18333: "HTTP Alt", 18334: "HTTP Alt", 18335: "HTTP Alt",
            18400: "HTTP Alt", 18444: "HTTP Alt", 18500: "HTTP Alt",
            18600: "HTTP Alt", 18605: "HTTP Alt", 18700: "HTTP Alt",
            18750: "HTTP Alt", 18769: "HTTP Alt", 18800: "HTTP Alt",
            18801: "HTTP Alt", 18802: "HTTP Alt", 18803: "HTTP Alt",
            18810: "HTTP Alt", 18811: "HTTP Alt", 18812: "HTTP Alt",
            18820: "HTTP Alt", 18821: "HTTP Alt", 18830: "HTTP Alt",
            18831: "HTTP Alt", 18832: "HTTP Alt", 18835: "HTTP Alt",
            18840: "HTTP Alt", 18850: "HTTP Alt", 18880: "HTTP Alt",
            18881: "HTTP Alt", 18882: "HTTP Alt", 18883: "HTTP Alt",
            18884: "HTTP Alt", 18885: "HTTP Alt", 18886: "HTTP Alt",
            18887: "HTTP Alt", 18888: "HTTP Alt", 18900: "HTTP Alt",
            18901: "HTTP Alt", 19000: "HTTP Alt", 19001: "HTTP Alt",
            19010: "HTTP Alt", 19020: "HTTP Alt", 19080: "HTTP Alt",
            19081: "HTTP Alt", 19090: "HTTP Alt", 19100: "HTTP Alt",
            19101: "HTTP Alt", 19102: "HTTP Alt", 19103: "HTTP Alt",
            19104: "HTTP Alt", 19105: "HTTP Alt", 19106: "HTTP Alt",
            19107: "HTTP Alt", 19108: "HTTP Alt", 19109: "HTTP Alt",
            19110: "HTTP Alt", 19130: "HTTP Alt", 19140: "HTTP Alt",
            19150: "HTTP Alt", 19200: "HTTP Alt", 19220: "HTTP Alt",
            19250: "HTTP Alt", 19283: "HTTP Alt", 19294: "HTTP Alt",
            19300: "HTTP Alt", 19302: "HTTP Alt", 19305: "HTTP Alt",
            19315: "HTTP Alt", 19350: "HTTP Alt", 19400: "HTTP Alt",
            19410: "HTTP Alt", 19412: "HTTP Alt", 19415: "HTTP Alt",
            19500: "HTTP Alt", 19501: "HTTP Alt", 19510: "HTTP Alt",
            19600: "HTTP Alt", 19601: "HTTP Alt", 19610: "HTTP Alt",
            19620: "HTTP Alt", 19630: "HTTP Alt", 19638: "HTTP Alt",
            19640: "HTTP Alt", 19700: "HTTP Alt", 19710: "HTTP Alt",
            19771: "HTTP Alt", 19772: "HTTP Alt", 19800: "HTTP Alt",
            19801: "HTTP Alt", 19810: "HTTP Alt", 19842: "HTTP Alt",
            19850: "HTTP Alt", 19900: "HTTP Alt", 19910: "HTTP Alt",
            19920: "HTTP Alt", 19930: "HTTP Alt", 19940: "HTTP Alt",
            19950: "HTTP Alt", 19960: "HTTP Alt", 19970: "HTTP Alt",
            19980: "HTTP Alt", 19990: "HTTP Alt", 20000: "HTTP Alt",
        }

    async def scan(self, domain: str, ports: Optional[list[int]] = None) -> dict:
        if ports is None:
            ports = self.common_ports

        try:
            ips = await self._resolve_domain(domain)
        except Exception as e:
            return {"domain": domain, "error": str(e), "ports": [], "open_count": 0}

        if not ips:
            return {"domain": domain, "error": "Could not resolve domain", "ports": [], "open_count": 0}

        all_open: dict = {}
        for ip in ips:
            all_open[ip] = []
            semaphore = asyncio.Semaphore(50)
            async def check_port(port: int, target_ip: str = ip) -> tuple:
                async with semaphore:
                    try:
                        _, writer = await asyncio.wait_for(
                            asyncio.open_connection(target_ip, port),
                            timeout=2
                        )
                        writer.close()
                        return (port, True)
                    except Exception:
                        return (port, False)

            tasks = [check_port(port) for port in ports]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            open_ports = []
            for result in results:
                if isinstance(result, tuple) and result[1]:
                    port = result[0]
                    service = self.service_map.get(port, "Unknown")
                    open_ports.append({"port": port, "service": service, "ip": ip})

            if open_ports:
                all_open[ip] = open_ports

        flat_ports = []
        seen_ports = set()
        for ip, ports in all_open.items():
            for p in ports:
                if p["port"] not in seen_ports:
                    seen_ports.add(p["port"])
                    flat_ports.append(p)

        flat_ports.sort(key=lambda x: x["port"])

        return {
            "domain": domain,
            "ips": ips,
            "ports": flat_ports,
            "open_count": len(flat_ports),
        }

    async def _resolve_domain(self, domain: str) -> list[str]:
        try:
            return list(set([addr[4][0] for addr in socket.getaddrinfo(domain, 80, socket.AF_INET)]))
        except Exception:
            return []
