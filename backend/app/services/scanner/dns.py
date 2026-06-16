import asyncio
import dns.resolver
import dns.zone
import socket
from typing import Optional


class DNSScanner:
    async def scan(self, domain: str) -> dict:
        result = {
            "domain": domain,
            "records": {},
            "zone_transfer": None,
            "spf": None,
            "dmarc": None,
            "dkim": None,
        }
        resolver = dns.resolver.Resolver()
        resolver.timeout = 5
        resolver.lifetime = 10

        record_types = ["A", "AAAA", "CNAME", "MX", "NS", "TXT", "SOA", "SRV", "CAA"]

        for rtype in record_types:
            try:
                answers = resolver.resolve(domain, rtype)
                records = [str(r) for r in answers]
                if records:
                    result["records"][rtype] = records
            except dns.resolver.NoAnswer:
                pass
            except dns.resolver.NXDOMAIN:
                pass
            except Exception:
                pass

        try:
            answers = resolver.resolve(f"_dmarc.{domain}", "TXT")
            result["dmarc"] = [str(r) for r in answers]
        except Exception:
            pass

        try:
            answers = resolver.resolve(f"default._domainkey.{domain}", "TXT")
            result["dkim"] = [str(r) for r in answers]
        except Exception:
            pass

        try:
            ns_records = result["records"].get("NS", [])
            for ns in ns_records[:3]:
                try:
                    ns_ip = socket.gethostbyname(ns)
                    xfr = dns.query.xfr(ns_ip, domain, timeout=5, lifetime=10)
                    zones = [str(r) for r in xfr]
                    if zones:
                        result["zone_transfer"] = {
                            "nameserver": ns,
                            "records": zones,
                            "vulnerable": True,
                        }
                        break
                except Exception:
                    continue
        except Exception:
            pass

        for rtype in ["A", "AAAA"]:
            ips = result["records"].get(rtype, [])
            if ips:
                rdns_results = []
                for ip in ips:
                    try:
                        hostname, _, _ = socket.gethostbyaddr(ip)
                        rdns_results.append({"ip": ip, "hostname": hostname})
                    except Exception:
                        rdns_results.append({"ip": ip, "hostname": None})
                result[f"reverse_dns_{rtype.lower()}"] = rdns_results

        return result
