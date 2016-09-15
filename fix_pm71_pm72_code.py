import os
os.chdir(r'D:\Google Drive\Documents\CaltechWork\platemaps\201608alloy')
for p in [r'J:\hte_jcap_app_proto\map\0071_04_0100_mp.txt', r'J:\hte_jcap_app_proto\map\0072_04_0100_mp.txt']:
    with open(p, mode='r') as f:
        lines=f.readlines()
    lines[1]=lines[1].replace(', I(fraction)', '')
    for i in range(2, len(lines)):
        l=lines[i]
        a, com, b=l.rpartition(',')
        b=b.strip()
        c=eval(b)
        if c>4:
            c*=10
        lines[i]='%s, %d\n' %(a, c)

    s=''.join(lines)
    pnew=os.path.split(p)[1][:-4]+'_codefixed.txt'
    with open(pnew, mode='w') as f:
        f.write(s)
