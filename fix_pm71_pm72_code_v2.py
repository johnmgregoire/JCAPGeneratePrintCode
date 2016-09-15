import os
os.chdir(r'D:\Google Drive\Documents\CaltechWork\platemaps\201608alloy')
for p in [r'J:\hte_jcap_app_proto\map\0071-04-0100-mp.txt', r'J:\hte_jcap_app_proto\map\0072-04-0100-mp.txt']:
    with open(p, mode='r') as f:
        lines=f.readlines()
    for i in range(2, len(lines)):
        l=lines[i]
        ll=l.split(', ')
        ll.pop(-2)
        lines[i]=', '.join(ll)

    s=''.join(lines)
    pnew=os.path.split(p)[1][:-4]+'_Iremovedfixed.txt'
    with open(pnew, mode='w') as f:
        f.write(s)
