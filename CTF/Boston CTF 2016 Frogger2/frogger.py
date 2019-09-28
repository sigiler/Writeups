primes = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,461,463,467,479,487,491,499,503,509,521,523,541,547,557,563,569,571,577,587,593,599,601,607,613,617,619,631,641,643,647,653,659,661,673,677,683,691,701,709,719,727,733,739,743,751,757,761,769,773,787,797,809,811,821,823,827,829,839,853,857,859,863,877,881,883,887,907,911,919,929,937,941,947,953,967,971,977,983,991,997,1009,1013,1019,1021]
targetstr = "Congratulations!  Treat yourself to some durians!"
#targetstr = "Nope!  You need to practice your fractions!"

def show_programs():
    programs = []
    #f = open("strings_factor_print.txt", "r")
    f = open("numbers.txt", "r")
    i = 0
    for line in f:
        num = int(line)
        programs.append(num)
        if i >= 0 and i <= 100:
            print(i)
            print(num2str_readable(num))
        
        i = i + 1


def simul():
    
    # prepare program
    f = open("numbers.txt", "r")
    lines = f.readlines()
    program = []
    for line in lines:
        program.append(int(line))
    
    # input
    input_str = ""
    
    # input str converted to int
    num = str2num_true(input_str) * 1019
    print(num)
    print(num2str(num))
    
    # execute vm
    divided = 1
    e=0
    while divided:
        divided = 0
        
        for i in range(0, len(program), 2):
            p1 = program[i]
            p2 = program[i+1]
            temp=num
            temp *= p1
            
            if (temp % p2) == 0:
                num = temp // p2
                divided = 1
                e+=1
                break
    
    print(num)
    print(num2str(num))
    
    
def solve_ctf():
    
    f = open("numbers.txt", "r")
    lines = f.readlines()
    program = []
    for line in lines:
        program.append(int(line))
    
    last = str2num(targetstr)
    
    current = last
    fixes = 1
    i=len(lines)-1
    # unmake vm execution
    """while i>1:
        p1 = program[i-1]
        p2 = program[i]
        i-=2
        current"""
    """"
    for i in range(len(lines)-2, 0, -2):
        
        p1 = program[i]
        p2 = program[i+1]
        vezes = 0
        while(1):
            vezes = vezes + 1
            print "vexes: " + str(vezes)
            temp=current
            temp*=p2
            if temp%p1==0:
                current=temp//p1
            else:
                break
       """
    divided=1
    while divided:
        divided = 0
        
        for i in range(len(lines)-2, 0, -2):
            p2 = program[i]
            p1 = program[i+1]
            temp=current
            temp *= p1
            
            if (temp % p2) == 0:
                current = temp // p2
                divided = 1
                break
    
    # ready to display flag
    flag=current
    flagstr = num2str_force(flag)
    print("flag: " + str(flag))
    print("flagstr: " + str(flagstr))
    import hashlib
    m = hashlib.md5()
    m.update(bytes(flagstr))
    flagmd5 = m.hexdigest()
    
    print("key:", flagstr)
    print("len of flagstr:", len(flagstr))
    print("BKPCTF{"+flagmd5+"}")


def test():
    print(str2num("gib flag"))
    print(num2str(1734287969434254662183182274789552069446956861672961563595535746575961423235664720542259787795389850093493838080989463837893547010191271267846058083132487304206277833226372893197402324722988740720523644879410358649163507833133620535841692931764803619111582609797056297831057365917256278600295116080403642033416763856121064627668121752350880088375210603574192101916384161988386909051432477969239845279695112155088555292934641885175874925557841441659032727243567545111159849021707187494129939679087965486147605249594043204331046516968997900265521825286757148800000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000))


def str2num_true(s):
    l = len(s)
    n = 1
    for i in range(len(s)):
        if min(l,84) <= i:
            break
        p = primes[i]
        e = ord(s[i])
        n = n * p**e
    return n

def str2num(s):
    n = 1
    for i in range(len(s)):
        p = primes[i]
        e = ord(s[i])
        n = n * p**e
    return n


def num2str(n):
    s = ''
    for p in primes:
        c = 0
        while (n % p) == 0:
            n = n//p
            c += 1
        if c != 0:
            s = s + chr(c)
        else:
            break
    return s


def num2str_force(n):
    s = ''
    for p in primes:
        c = 0
        while (n % p) == 0:
            n = n//p
            c += 1
        if c != 0:
            s = s + chr(c)
        else:
            s = s + chr(c)
    return s


def num2str_readable(n):
    l = []
    for p in primes:
        c = 0
        while (n % p) == 0:
            n = n//p
            c += 1
        l.append(str(c))
    if n != 1:
        assert(False)
        assert(True)
    return ",".join(l)
    


#test()
#show_programs()
#simul()
solve_ctf()
