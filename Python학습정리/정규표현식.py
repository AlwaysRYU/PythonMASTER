# 0. 정규표현식이란?


# 복잡한 문자열을 처리할 때 사용하는 기법.
# 참고 : https://wikidocs.net/1642

'''
파이썬의 고유문법이 아니라, 
문자열을 처리하는 모든 곳에서 사용한다.
정규표현식을 배우는 것은 파이썬을 배우는 것과는
또 다른 영역의 과제이다.
'''

# Q : 주민등록번호를 포함하는 텍스트가 있다. 이텍스트에 포함된 모든 주민번호의 뒷자리를 *로 변경하자. 

# 정규식을 모를 때
'''
1. 텍스트를 공백으로 나누고 split
2. 단어가 주민번호 형식인지? 맞다면 *
3. 다시 합친다.
'''

data = """
park 800905-1049118
kim  700905-1059119
"""

result = []
for line in data.split("\n"):
    word_result = []
    for word in line.split(" "):
        #isdigit : 숫자인지 True로 반환
        if len(word) == 14 and word[:6].isdigit() and word[7:].isdigit():
            word = word[:6] + "-" + "*******"
        word_result.append(word)
    result.append(" ".join(word_result))
print("\n".join(result))

# 정규식을 사용하면

import re

pat = re.compile("(\d{6})[-]\d{7}")
pat = re.compile("(\d{6})[-]\d{7}")

print(pat.sub("\g<1>-*******", data))

# 이렇게 표현 가능하다.



# 1. 메타문자
'''
정규표현식에서는 메타문자를 사용한다.
메타문자란, 원래 그문자가 가진 뜻이 아닌 특별한 용도로사용하는 문자를 말한다.
. ^ $ * ? + { } [ ] \ | ( )
정규표현식의 위의 문자를 사용하면 특별한 의미를 갖게 된다.
'''

# 1-1. [] 문자클래스
'''
의미: [ ] 사이의 문자들과 매치
    어떠한 문자든 [] 들어갈수 있다.
    ex : [abc] -> a b c 중 한개의 문자와 매치한다. 
    'a' 는 'a'가 있으므로 매치
    'before' 는 'b'가 있으므로 매치
    'dude' 는 매치하지 않는다.
특징1: -
    []사이에 - 를 이용하면 문자 사이의 범위를 의미한다.
    [a-c]라는 정규표현식은 [abc]와 동일하다.
    [0-5]는 [012345]와 동일하다.
    ex : [a-zA-Z] 알파벳 모두 [0-9] 숫자
특징2: ^
    []안에는 어떠한 문자나 메타문자도 사용할 수 있지만, ^는 주의하자.
    ^는 not 의 의미를 가지고 있다.
    ex : [^0-9] : 숫자가 아닌 문자만 매치된다.
자주 사용하는 문자 클래스:
    [0-9] 또는 [a-zA-Z] 등은 무척 자주 사용하는 정규 표현식이다. 이렇게 자주 사용하는 정규식은 별도의 표기법으로 표현할 수 있다. 다음을 기억해 두자.
    \d - 숫자와 매치, [0-9]와 동일한 표현식이다.
    \D - 숫자가 아닌 것과 매치, [^0-9]와 동일한 표현식이다.
    \s - whitespace 문자와 매치, [ \t\n\r\f\v]와 동일한 표현식이다. 맨 앞의 빈 칸은 공백문자(space)를 의미한다.
    \S - whitespace 문자가 아닌 것과 매치, [^ \t\n\r\f\v]와 동일한 표현식이다.
    \w - 문자+숫자(alphanumeric)와 매치, [a-zA-Z0-9_]와 동일한 표현식이다.
    \W - 문자+숫자(alphanumeric)가 아닌 문자와 매치, [^a-zA-Z0-9_]와 동일한 표현식이다.
    대문자로 사용된 것은 소문자의 반대임을 추측할 수 있다.
'''

# 1-2. . Dot
'''
의미:
    줄바꿈 문자인 \n을 제외한 모든 문자와 매치됨을 의미한다.
    ex : a.b 는 a + 모든문자 + b 이다.
    'aaab' -> 매치
    'a0b' -> 매치
    'abc' -> 한글자라도 있어야하므로 매치되지 않는다.
주의:
    a[.]b
    는, 진짜 .을 의미한다.
'''

# 1-3. * 반복
'''
의미:
    반복을 의미한다.
    *바로앞에있는 문자 a가 0부터 무한으로 반복될 수 있다는 의미.
    ex : ca*t 의 정규식은
    ct -> 매치
    cat -> 매치
    caaaaat -> 매치
'''

# 1-4. + 반복
'''
의미:
    반복을 의미한다.
    단, 1번이상 반복해야한다.
    *가 반복횟수 0부터라면 +는 반복횟수 1부터이다. 
    ca+t의 정규식은, a를 한번이상 반복이다.
    ct -> 매치안됨.
    caaat -> 매치
'''

# 1-5. {} 반복횟수를 제한
'''
의미 : 
    반복횟수를 고정할 수 있다.
    {m,n} 반복횟수가 m부터 n까지 매치할 수 있다.
    {3,} -> 반복횟수가 3이상인 경우
    {,3} -> 반복횟수가 3이하인 경우.
    {1,} -> +
    {0,} -> * 
    ex : ca{2}t : c a를 두번이상 반복 t
    ca{2,5}t 는 a를 2~5 번반복만 매치.
'''

# 1-6. ?
'''
의미:
    {0,1}를 의미한다.
    ab?c -> 있어도되고, 없어도 된다.
    abc는 b가 1번이상이라 매치
    ac 는 b가 0번이라 매치.
'''

# 2. re 모듈
'''
import re 가필요하다.
regular expression 
'''

import re
p = re.compile('ab*')
'''
패턴 : 정규식을 컴파일한 결과
사용방법 :
    re.compile을 사용하여 정규표현식을 컴파일 한다.
    위에서는 ab*를 컴파일한다.
    re.compile의 결과로 돌려주는 객체 p = 컴파일된 패턴 객체 를사용하여 그이후의 작업을 수행한다.
    옵션을 주는것도 가능하다.
'''

# 3. 정규식을 이용한 문자열 검색
'''
컴파일된 패턴 객체를 사용하여 문자열 검색을 수행한다.
메소드:
    match() : 문자열의 처음부터 정규식과 매치 되는가?
    search() : 문자열전체를 검색하여 정규식과 매치되는지 조사한다.
    findall() : 정규식과 매치되는 모든 문자열(substring)을 리스트로 돌려준다.
    finditer() : 정규식과 매치되는 모든 문자열(substring)을 반복 가능한 객체로 돌려준다.
'''

# 3-0. 패턴생성
p = re.compile('[a-z]+') # 뜻 : abcd...z까지  1번이상 반복하는가?

# 3-1. match
'''
의미 :
    문자열이 처음부터 정규식과 매치가 되는가?
'''
print("match 예시 : ")
match = p.match("python")  # 정규식에 부합하는 지 팔별한다. python은 정규식에 부합한다.
print(match)
match = p.match("3 python") # 3 python 은 정규식에 부합하지 않는다.
print(match)
print()

'''
보통 이런식으로 작성한다.
    p = re.compile(정규표현식)
    m = p.match( 'string goes here' )
    if m:
        print('Match found: ', m.group())
    else:
        print('No match')
'''

# 3-2. search()
'''
의미 :
    match와 비슷하지만,
    문자열의 전체를 검색한다.
'''
print("search")
p = re.compile("[a-z]+")
search = p.search("3 python")
print(search)
print()

# 3-3. findall()
'''
의미 :
    문자열의 각각 단어를 각각 정규식(p , 여기서는 [a-z]+)와 매치해서
    리스트로 되돌려준다.
    매치되는 것만 되돌려 준다.
'''
print("findall 예시 : ")
p = re.compile("[a-z]+")
findall = p.findall("only a fool could walk away from me this time cloud 9 ") 
print(findall)
print()

# 3-4. finditer()
'''
의미:
    findall과 동일하지만, 결과로 반복가능한 객체 (iterator object)를 돌려줌.
    반복가능한 객체가 포함하는 각각의 요소는 match객체이다.
    역시 매치 되는 것만 알려준다.
'''
print("finditer 예시 : ")
p = re.compile("[a-z]+")
finditer = p.finditer("I need to find out where I am before I reach the stars")
print(finditer)
for r in finditer :
    print(r)
print()

# 4. match객체의 메소드
'''
개념:
    match 메소드 search 메소드를 수행한 결과로 돌려주는 match객체를 다루는다.
    앞에서 정규식을 사용한 문자열 검색을 수행하면서 어떤 문자열인지, 인덱스는 무엇인지 알려준다.
    group()	매치된 문자열을 돌려준다.
    start()	매치된 문자열의 시작 위치를 돌려준다.
    end()	매치된 문자열의 끝 위치를 돌려준다.
    span()	매치된 문자열의 (시작, 끝)에 해당하는 튜플을 돌려준다.
'''
print("match객체의 메소드")
print("정규표현식 컴파일된 패턴객체 p  = [a-z]+ / m은 match 객체")
m = p.match("python")

# 4-1. group() : 매치된 문자열을 알려준다.
print("group() : ")
print(m.group())

# 4-2. start() : 매치된 문자열의 시작 위치를 알려준다.
print("start() : ")
print(m.start())

# 4-3. end() : 매치된 문자열의 끝 위치를 알려준다.
print("end() : ")
print(m.end())

# 4-4. span() : 매치된 문자열의 시작과 끝에 해당하는 튜플을 알려준다.
print("span() : ")
print(m.span())
print()
print()

# 4-5. sub() : 해당하는문자열을 제거
re.sub('apple|orange', 'fruit', 'apple box orange tree')
# 문자열에서 apple, orange를 찾아서, fruit로 바꾼다.


# 팁 : 매치하는 과정을 다음과 같이축약할 수 있다.
m = re.match('[a-z]+', "python")

# 5. 메타문자
'''
문자열 소비가 없는 메타 문자

'''

# 5-1. | OR
# A|B 정규식이 있다면 A 또는 B가 의미가 된다.
p = re.compile('Crow|Servo')
m = p.match('CrowHello')
print(m)

# 5-2. ^
'''
의미:
    문자열 맨처음과 일치하는가?
'''
print(re.search('^Life', 'Life is too short'))
print(re.search('^Life', 'My Life'))


# 6. 정규식 컴파일 옵션
'''
컴파일할 때 옵션을 사용할 수 있다.

'''


'''
정규표현식(Regular Expressions) 문법 정리

기본 메타 문자 

    . 모든 문자와 일치 
    | 왼쪽 혹은 오른쪽과 일치 
    [] 문자 집합 구성원 중 하나와 일치 
    [^] 문자 집합 구성원을 제외하고 일치
    - 범위 정의 ( [A-Z]와 같은 형태 )
    \ 다음에 오는 문자를 이스케이프
수량자
    * 문자가 없는 경우나 하나 이상 연속하는 문자 찾기
    *? 게으른 * 문자
    + 문자 하나 이상 찾기
    +? 게으른 + 문자
    ? 문자가 없거나 하나인 문자 찾기
    {n} 정확히 요소와 n번 일치
    {m,n} 요소와 m에서 n번 일치
    {n,} 요소와 n번 이상 일치
    {n,}?
    게으른 {n,}

위치 지정 

^

문자열의 시작과 일치

\A

문자열의 시작과 일치

$

문자열의 끝과 일치

\Z

문자열의 끝과 일치

\<

단어의 시작과 일치

\>

단어의 끝과 일치

\b

단어 경계와 일치

\B

\b 와 반대로 일치

특수한 문자

[\b]

역스페이스 

\c

제어문자와 일치

\d

모든 숫자와 일치

\D

\d 와 반대

\f

페이지 넘기기(form feed)

\n

줄바꿈

\r

캐리지 리턴

\s

공백 문자와 일치

\S

\s 와 반대로 일치

\t

탭

\v

수직 탭

\w

영숫자 문자나 밑줄과 일치

\W

\w 와 반대로 일치

\x

16진수 숫자와 일치

\0

8진수 숫자와 일치

역참조와 전후방 탐색

()

하위 표현식 정의

\1

첫 번째 일치한 하위 표현식. 두번째 일치한 하위 표현식은 \2 로 표기하는 방식

?=

전방탐색

?<=

후방탐색

?!

부정형 전방탐색

?	
부정형 후방탐색

?(backreference)true

조건 지정

?(backreference)true|false

else 표현식 조건 지정

 대소문자 변환

\E 

\L 혹은 \U 변환을 끝냄

\l

다음에 오는 글자를 소문자로 변환

\L

\E 를 만날 때까지 모든 문자를 소문자로 변환

\u

다음에 오는 글자를 대문자로 변환

\U

\E 를 만날 때까지 모든 문자를 대문자로 변환

변경자

(?m) 

다중행 모드

'''