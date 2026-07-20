import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'namakkal_pgr.settings')
django.setup()

from django.contrib.auth.models import User
from complaints.models import Zone, Ward, Area, ComplaintStatus, Officer

def seed_db():
    print("Seeding database...")

    # 1. Create Statuses
    statuses = ['Submitted', 'Assigned', 'In Progress', 'Resolved', 'Closed']
    for status_name in statuses:
        status, created = ComplaintStatus.objects.get_or_create(name=status_name)
        if created:
            print(f"Created status: {status_name}")

    # 2. Create Zones
    zones_data = [
        {'name': 'Zone I (North)', 'code': 'ZN-01'},
        {'name': 'Zone II (East)', 'code': 'ZN-02'},
        {'name': 'Zone III (South)', 'code': 'ZN-03'},
        {'name': 'Zone IV (West)', 'code': 'ZN-04'},
    ]
    zones = {}
    for z_info in zones_data:
        zone, created = Zone.objects.get_or_create(name=z_info['name'], code=z_info['code'])
        zones[z_info['code']] = zone
        if created:
            print(f"Created zone: {zone.name}")

    # 3. Create Wards & Areas
    # Zone 1 Wards: 1, 2, 3, 4
    # Zone 2 Wards: 5, 6, 7
    # Zone 3 Wards: 8, 9, 10, 11
    # Zone 4 Wards: 12, 13, 14, 15
    wards_data = {
        'ZN-01': [
            {'number': 1, 'name': 'Thillaipuram', 'areas': ['Thillaipuram Extension', 'Salem Road Cross', 'Cooperative Colony']},
            {'number': 2, 'name': 'Ganesapuram', 'areas': ['Ganesapuram Main', 'Kamaraj Nagar', 'Anna Nagar']},
            {'number': 3, 'name': 'Kottai', 'areas': ['Kottai Street', 'Anjaneyar Temple Street', 'Fort Road']},
            {'number': 4, 'name': 'Nallipalayam', 'areas': ['Nallipalayam Village', 'Bypass Link Road', 'Vetri Nagar']},
        ],
        'ZN-02': [
            {'number': 5, 'name': 'Mohanur Road', 'areas': ['Mohanur Road Junction', 'South Colony', 'Teacher\'s Colony']},
            {'number': 6, 'name': 'Senthamangalam', 'areas': ['Senthamangalam Main', 'Bharathi Nagar', 'SPB Colony']},
            {'number': 7, 'name': 'Rathinasamy Puram', 'areas': ['Rathinasamy Puram North', 'Rathinasamy Puram South']},
        ],
        'ZN-03': [
            {'number': 8, 'name': 'Paramathi Road', 'areas': ['Paramathi Road Corner', 'Velur Road Cross', 'GGP Nagar']},
            {'number': 9, 'name': 'Keerambur', 'areas': ['Keerambur Junction', 'Anna Silai Circle', 'Housing Board']},
            {'number': 10, 'name': 'SP Pudur', 'areas': ['SP Pudur East', 'SP Pudur West', 'Kaveri Nagar']},
            {'number': 11, 'name': 'R.P. Pudur', 'areas': ['RP Pudur Main', 'Gandhi Nagar', 'Vallalar Nagar']},
        ],
        'ZN-04': [
            {'number': 12, 'name': 'Trichi Road', 'areas': ['Trichi Road Flyover', 'Srinivasa Nagar', 'Vasantha Nagar']},
            {'number': 13, 'name': 'Erulapatty', 'areas': ['Erulapatty Main', 'Karuppar Temple St', 'MGR Nagar']},
            {'number': 14, 'name': 'Kallangulam', 'areas': ['Kallangulam Lake road', 'Bharathiar Street']},
            {'number': 15, 'name': 'Mudalaipatti', 'areas': ['Mudalaipatti Bypass', 'NH Link Road', 'Industrial Estate']},
        ]
    }

    for zone_code, wards_list in wards_data.items():
        zone = zones[zone_code]
        for w_info in wards_list:
            ward, created = Ward.objects.get_or_create(
                zone=zone, 
                number=w_info['number'], 
                defaults={'name': w_info['name']}
            )
            if created:
                print(f"Created Ward {ward.number} ({ward.name})")
            
            for area_name in w_info['areas']:
                area, a_created = Area.objects.get_or_create(ward=ward, name=area_name)
                if a_created:
                    print(f"  Created Area: {area_name}")

    # 4. Create default admin superuser if not exists
    if not User.objects.filter(username='admin').exists():
        admin_user = User.objects.create_superuser('admin', 'admin@namakkalcorporation.org', 'admin123')
        print("Created Superuser: admin / admin123")
        
        # Make admin a default officer for assignments
        officer, created = Officer.objects.get_or_create(
            user=admin_user,
            defaults={
                'name': 'Shri. K. Ramasamy',
                'email': 'commr.namakkal@tn.gov.in',
                'mobile': '06286-221777',
                'department': 'General',
                'zone': zones['ZN-01']
            }
        )
        if created:
            print(f"Created default Officer for admin: {officer.name}")
    else:
        print("Admin user already exists.")

    print("Seeding completed successfully!")

if __name__ == '__main__':
    seed_db()
