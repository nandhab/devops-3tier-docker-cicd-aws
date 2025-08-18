#!/usr/bin/env python3
"""
Generate a self-signed TLS certificate and private key.

Examples:
  python gen_self_signed_cert.py --hostnames localhost,127.0.0.1,::1 \
      --out-dir frontend/certs/selfsigned --days 365 --key-size 4096

Outputs:
  <basename>.crt  (PEM X.509 certificate)
  <basename>.key  (unencrypted PEM private key)
"""

import argparse
import ipaddress
from pathlib import Path
from datetime import datetime, timedelta

from cryptography import x509
from cryptography.x509.oid import NameOID, ExtendedKeyUsageOID
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa


def parse_args():
    p = argparse.ArgumentParser(description="Create a self-signed TLS certificate.")
    p.add_argument(
        "-H", "--hostnames",
        required=True,
        help="Comma-separated hostnames and/or IPs to include in SAN (e.g. 'localhost,127.0.0.1,::1,my.dev').",
    )
    p.add_argument(
        "-o", "--out-dir",
        default=".",
        help="Output directory for .crt and .key (default: current directory).",
    )
    p.add_argument(
        "-b", "--basename",
        default=None,
        help="Output file base name (default: first hostname).",
    )
    p.add_argument(
        "--days",
        type=int,
        default=365,
        help="Validity period in days (default: 365).",
    )
    p.add_argument(
        "--key-size",
        type=int,
        default=2048,
        choices=(2048, 3072, 4096),
        help="RSA key size (default: 2048).",
    )
    return p.parse_args()


def is_ip(value: str) -> bool:
    try:
        ipaddress.ip_address(value)
        return True
    except ValueError:
        return False


def main():
    args = parse_args()

    hosts = [h.strip() for h in args.hostnames.split(",") if h.strip()]
    if not hosts:
        raise SystemExit("No hostnames provided.")
    first = hosts[0]
    basename = args.basename or first

    out_dir = Path(args.out_dir).expanduser().resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    key_path = out_dir / f"{basename}.key"
    crt_path = out_dir / f"{basename}.crt"

    # Generate RSA private key
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=args.key_size)

    # Subject / Issuer (self-signed)
    subject = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, first),
        # Add these if you like:
        # x509.NameAttribute(NameOID.ORGANIZATION_NAME, "Local Dev"),
        # x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
    ])

    # Build SAN list (DNSName or IPAddress)
    san_entries = []
    for h in hosts:
        if is_ip(h):
            san_entries.append(x509.IPAddress(ipaddress.ip_address(h)))
        else:
            san_entries.append(x509.DNSName(h))

    now = datetime.utcnow()
    cert_builder = (
        x509.CertificateBuilder()
        .subject_name(subject)
        .issuer_name(subject)  # self-signed
        .public_key(private_key.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(now - timedelta(minutes=5))
        .not_valid_after(now + timedelta(days=args.days))
        .add_extension(x509.SubjectAlternativeName(san_entries), critical=False)
        .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
        .add_extension(
            x509.KeyUsage(
                digital_signature=True,
                content_commitment=False,
                key_encipherment=True,
                data_encipherment=False,
                key_agreement=False,
                key_cert_sign=False,
                crl_sign=False,
                encipher_only=False,
                decipher_only=False,
            ),
            critical=True,
        )
        .add_extension(
            x509.ExtendedKeyUsage([ExtendedKeyUsageOID.SERVER_AUTH]),
            critical=False,
        )
    )

    certificate = cert_builder.sign(private_key=private_key, algorithm=hashes.SHA256())

    # Write private key (PEM, unencrypted)
    with open(key_path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,  # ".key" friendly
                encryption_algorithm=serialization.NoEncryption(),
            )
        )

    # Write certificate (PEM)
    with open(crt_path, "wb") as f:
        f.write(certificate.public_bytes(serialization.Encoding.PEM))

    print(f"Wrote key: {key_path}")
    print(f"Wrote cert: {crt_path}")
    print("\nTips:")
    print(" - In NGINX, use:")
    print(f"     ssl_certificate     {crt_path};")
    print(f"     ssl_certificate_key {key_path};")
    print(" - For local Docker NGINX, mount the output directory into /etc/ssl/localcerts.")
    print(" - On Windows, to trust locally in Chrome/Edge, you can import the .crt into Trusted Root CAs.")


if __name__ == "__main__":
    main()
