import pytest

from src.manager import Manager
from src.models import Parameters, Transfer


def test_total_due_pln():
    manager = Manager(Parameters())
    apartment_settlement = manager.get_settlement('apart-polanka', 2025, 1)
    
    assert apartment_settlement is not None

    tenants_settlements = manager.create_tenants_settlements(apartment_settlement)
    
    assert isinstance(tenants_settlements, list)
    assert tenants_settlements, "Nie ma listy dluznikow"

    total_tenants_due = sum(tenant.total_due_pln for tenant in tenants_settlements)
   
    assert total_tenants_due == pytest.approx(apartment_settlement.total_due_pln)


def test_get_tax():
    manager = Manager(Parameters())
    manager.transfers = [
        Transfer(
            amount_pln=2500.0,
            date="2025-01-04",
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-1'
        ),
        Transfer(

            amount_pln=2500.0,
            date="2025-01-05",
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-2'
        ),
        Transfer(
            amount_pln=2500.0,
            date="2025-01-06",
            settlement_year=2025,
            settlement_month=1,
            tenant='tenant-3'
        ),
    ]
    tax = manager.get_tax(2025, 1,0.085)
    assert tax == 638
    tax = manager.get_tax(2025, 1 ,0.10)
    assert tax == 750   

def test_annual_raport():
    manager = Manager(Parameters())
    apartment_key = "apart-polanka"
    year = 2025
    annual_report = manager.get_annual_report(apartment_key,year)
    assert len(annual_report) > 0
    total_annual_due = sum(report["total_due_pln"] for report in annual_report)
    expected_total_due = sum(manager.get_apartment_costs(apartment_key, year, month) for month in range(1, 13))
    assert total_annual_due == expected_total_due
