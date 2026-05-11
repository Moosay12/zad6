import pytest

from src.manager import Manager
from src.models import Parameters
def test_total_due_pln():
    manager = Manager(Parameters())
    apartment_settlement = manager.get_settlement('apart-polanka', 2025, 1)
    
    assert apartment_settlement is not None

    tenants_settlements = manager.create_tenants_settlements(apartment_settlement)
    
    assert isinstance(tenants_settlements, list)
    assert tenants_settlements, "Expected at least one tenant settlement"

    total_tenants_due = sum(tenant.total_due_pln for tenant in tenants_settlements)
   
    assert total_tenants_due == pytest.approx(apartment_settlement.total_due_pln)
