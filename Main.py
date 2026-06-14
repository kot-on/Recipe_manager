from Database.DB_backup import check_integrity

if not check_integrity():
    print("ВНИМАНИЕ! База данных была изменена извне!")
