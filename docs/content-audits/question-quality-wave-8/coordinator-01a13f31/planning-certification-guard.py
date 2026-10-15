"""Acquire planning lease BEFORE an existing certificate helper writes code registry.

The existing helper reacquires the same owner and releases its lease on completion.
This outer guard only releases a still-owned lease when that helper exits early.
It never recovers, expires, or releases another owner's lease.
"""
def certify_preleased(module, *args, **kwargs):
    owner = module.O
    with module.flow.locked():
        module.flow.lease('acquire', 'planning', owner)
    try:
        return module.certify(*args, **kwargs)
    finally:
        with module.flow.locked():
            lease_file = module.P / '.flow-leases.json'
            leases = module.read(lease_file) if lease_file.exists() else {}
            if leases.get('planning', {}).get('owner') == owner:
                module.flow.lease('release', 'planning', owner)
