MERCHANTS = [
    {
        "id": "M001",
        "name": "Acme Fitness",
        "industry": "Fitness",
        "monthly_revenue": 485000,
        "customers": 1240,
    },
    {
        "id": "M002",
        "name": "StyleBox",
        "industry": "Fashion",
        "monthly_revenue": 372000,
        "customers": 980,
    },
    {
        "id": "M003",
        "name": "TechNova",
        "industry": "Software",
        "monthly_revenue": 615000,
        "customers": 1540,
    },
    {
        "id": "M004",
        "name": "FreshCart",
        "industry": "Grocery",
        "monthly_revenue": 294000,
        "customers": 1870,
    },
    {
        "id": "M005",
        "name": "EduPro",
        "industry": "Education",
        "monthly_revenue": 418000,
        "customers": 860,
    },
    {
        "id": "M006",
        "name": "CloudKitchen",
        "industry": "Food",
        "monthly_revenue": 256000,
        "customers": 1430,
    },
    {
        "id": "M007",
        "name": "UrbanThreads",
        "industry": "Fashion",
        "monthly_revenue": 341000,
        "customers": 1120,
    },
    {
        "id": "M008",
        "name": "MediPlus",
        "industry": "Healthcare",
        "monthly_revenue": 527000,
        "customers": 920,
    },
]


TRANSACTIONS = [

    # =====================================================
    # M001 — ACME FITNESS
    # Duplicate payment + failed renewal + abandoned payment
    # =====================================================

    {
        "id": "TX1001",
        "merchant": "M001",
        "customer": "C101",
        "amount": 12400,
        "status": "success",
        "type": "payment",
        "timestamp": "2026-09-04T10:42:11",
    },
    {
        "id": "TX1002",
        "merchant": "M001",
        "customer": "C101",
        "amount": 12400,
        "status": "success",
        "type": "payment",
        "timestamp": "2026-09-04T10:42:54",
    },
    {
        "id": "TX1003",
        "merchant": "M001",
        "customer": "C114",
        "amount": 7900,
        "status": "failed",
        "type": "subscription_renewal",
        "timestamp": "2026-09-04T09:18:00",
    },
    {
        "id": "TX1004",
        "merchant": "M001",
        "customer": "C129",
        "amount": 5600,
        "status": "abandoned",
        "type": "payment",
        "timestamp": "2026-09-04T08:15:00",
    },


    # =====================================================
    # M002 — STYLEBOX
    # Failed renewals + duplicate payment
    # =====================================================

    {
        "id": "TX2001",
        "merchant": "M002",
        "customer": "C205",
        "amount": 8200,
        "status": "failed",
        "type": "subscription_renewal",
        "timestamp": "2026-09-04T09:15:00",
    },
    {
        "id": "TX2002",
        "merchant": "M002",
        "customer": "C217",
        "amount": 6500,
        "status": "failed",
        "type": "subscription_renewal",
        "timestamp": "2026-09-04T09:42:00",
    },
    {
        "id": "TX2003",
        "merchant": "M002",
        "customer": "C223",
        "amount": 14900,
        "status": "success",
        "type": "payment",
        "timestamp": "2026-09-04T11:02:10",
    },
    {
        "id": "TX2004",
        "merchant": "M002",
        "customer": "C223",
        "amount": 14900,
        "status": "success",
        "type": "payment",
        "timestamp": "2026-09-04T11:03:02",
    },


    # =====================================================
    # M003 — TECHNOVA
    # Abandoned payments + duplicate payment
    # =====================================================

    {
        "id": "TX3001",
        "merchant": "M003",
        "customer": "C309",
        "amount": 6700,
        "status": "abandoned",
        "type": "payment",
        "timestamp": "2026-09-04T08:30:00",
    },
    {
        "id": "TX3002",
        "merchant": "M003",
        "customer": "C318",
        "amount": 18200,
        "status": "abandoned",
        "type": "payment",
        "timestamp": "2026-09-04T08:44:00",
    },
    {
        "id": "TX3003",
        "merchant": "M003",
        "customer": "C327",
        "amount": 22500,
        "status": "success",
        "type": "payment",
        "timestamp": "2026-09-04T10:12:01",
    },
    {
        "id": "TX3004",
        "merchant": "M003",
        "customer": "C327",
        "amount": 22500,
        "status": "success",
        "type": "payment",
        "timestamp": "2026-09-04T10:12:48",
    },


    # =====================================================
    # M004 — FRESHCART
    # Duplicate refunds
    # =====================================================

    {
        "id": "TX4001",
        "merchant": "M004",
        "customer": "C412",
        "amount": 4500,
        "status": "refunded",
        "type": "payment",
        "timestamp": "2026-09-04T07:20:00",
    },
    {
        "id": "TX4002",
        "merchant": "M004",
        "customer": "C412",
        "amount": 4500,
        "status": "refunded",
        "type": "payment",
        "timestamp": "2026-09-04T07:21:00",
    },
    {
        "id": "TX4003",
        "merchant": "M004",
        "customer": "C431",
        "amount": 3800,
        "status": "abandoned",
        "type": "payment",
        "timestamp": "2026-09-04T08:10:00",
    },
    {
        "id": "TX4004",
        "merchant": "M004",
        "customer": "C447",
        "amount": 7200,
        "status": "failed",
        "type": "subscription_renewal",
        "timestamp": "2026-09-04T09:05:00",
    },


    # =====================================================
    # M005 — EDUPRO
    # Failed renewals + abandoned payment
    # =====================================================

    {
        "id": "TX5001",
        "merchant": "M005",
        "customer": "C512",
        "amount": 5900,
        "status": "failed",
        "type": "subscription_renewal",
        "timestamp": "2026-09-04T06:45:00",
    },
    {
        "id": "TX5002",
        "merchant": "M005",
        "customer": "C526",
        "amount": 8900,
        "status": "failed",
        "type": "subscription_renewal",
        "timestamp": "2026-09-04T07:12:00",
    },
    {
        "id": "TX5003",
        "merchant": "M005",
        "customer": "C539",
        "amount": 12500,
        "status": "abandoned",
        "type": "payment",
        "timestamp": "2026-09-04T08:25:00",
    },


    # =====================================================
    # M006 — CLOUDKITCHEN
    # Duplicate payment + abandoned payment
    # =====================================================

    {
        "id": "TX6001",
        "merchant": "M006",
        "customer": "C620",
        "amount": 3100,
        "status": "abandoned",
        "type": "payment",
        "timestamp": "2026-09-04T06:10:00",
    },
    {
        "id": "TX6002",
        "merchant": "M006",
        "customer": "C633",
        "amount": 4200,
        "status": "success",
        "type": "payment",
        "timestamp": "2026-09-04T07:05:01",
    },
    {
        "id": "TX6003",
        "merchant": "M006",
        "customer": "C633",
        "amount": 4200,
        "status": "success",
        "type": "payment",
        "timestamp": "2026-09-04T07:05:46",
    },


    # =====================================================
    # M007 — URBANTHREADS
    # Duplicate refund + failed renewal
    # =====================================================

    {
        "id": "TX7001",
        "merchant": "M007",
        "customer": "C712",
        "amount": 6800,
        "status": "refunded",
        "type": "payment",
        "timestamp": "2026-09-04T08:30:00",
    },
    {
        "id": "TX7002",
        "merchant": "M007",
        "customer": "C712",
        "amount": 6800,
        "status": "refunded",
        "type": "payment",
        "timestamp": "2026-09-04T08:31:00",
    },
    {
        "id": "TX7003",
        "merchant": "M007",
        "customer": "C728",
        "amount": 7600,
        "status": "failed",
        "type": "subscription_renewal",
        "timestamp": "2026-09-04T09:40:00",
    },


    # =====================================================
    # M008 — MEDIPLUS
    # Duplicate payment + failed renewal + abandoned
    # =====================================================

    {
        "id": "TX8001",
        "merchant": "M008",
        "customer": "C812",
        "amount": 15600,
        "status": "success",
        "type": "payment",
        "timestamp": "2026-09-04T08:02:01",
    },
    {
        "id": "TX8002",
        "merchant": "M008",
        "customer": "C812",
        "amount": 15600,
        "status": "success",
        "type": "payment",
        "timestamp": "2026-09-04T08:02:39",
    },
    {
        "id": "TX8003",
        "merchant": "M008",
        "customer": "C825",
        "amount": 9200,
        "status": "failed",
        "type": "subscription_renewal",
        "timestamp": "2026-09-04T09:15:00",
    },
    {
        "id": "TX8004",
        "merchant": "M008",
        "customer": "C839",
        "amount": 11400,
        "status": "abandoned",
        "type": "payment",
        "timestamp": "2026-09-04T10:05:00",
    },
]