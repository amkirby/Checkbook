import Checkbook as C
cb = C.Checkbook()
cb.add(["9/1/2015","Credit","this is a test", 100.98])
cb.add(["9/1/2015","Debit","this is a test2", -45.45])
cb.add(["9/1/2015","Credit","this is a test3", 56.76])
cb.add(["9/1/2015","Debit","this is a test4", -12.23])
cb.add(["9/1/2015","Debit","this is a test5", -1.00])
cb.add(["9/1/2015","Credit","this is a test6", 56])
cb.add(["9/1/2015","Debit","this is a test7", -20])
cb.add(["9/1/2015","Debit","this is a test8", -34.89])
# cb.save()
# cb.load()
print(cb)

lis = cb.getTransactionType("Credit")
for elem in lis:
    print(elem)

print()
print()

lis = cb.getTransactionType("Debit")
for elem in lis:
    print(elem)


