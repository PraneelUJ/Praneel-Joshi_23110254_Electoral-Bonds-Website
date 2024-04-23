import mysql.connector as con
from flask import Flask,render_template,request
mydb=con.connect(host='localhost',user='root',passwd='tanishq20@5',database='electionbonddcc')
cursor=mydb.cursor()
app=Flask(__name__)
cursor.execute("Show columns from Redemption_Details")
c1=cursor.fetchall()
cursor.execute("Show columns from Purchase_Details")
c2=cursor.fetchall()
for i in range(len(c1)):
    c1[i]=c1[i][0]
for i in range(len(c2)):
    c2[i]=c2[i][0]
cursor.execute("Select distinct `Name of the Purchaser` from Purchase_Details")
name=list(cursor.fetchall())
for i in range(len(name)):
    
    name[i]=''.join(name[i])
# for i in c2:
#     if i not in c1:
#         c1.append(i)
c1=c1+c2[1:4]+c2[6:]
cursor.execute("Select distinct `Name of the Political Party` from Redemption_Details")
party=list(cursor.fetchall())
for i in range(len(party)):
    
    party[i]=''.join(party[i])
@app.route("/",methods=["GET","POST"])
def data():
    return render_template ("index.html",purchaser=name,party=party)

@app.route("/home",methods=["POST","GET"])
def home():
    if request.method=="POST":
        a=(request.form["nm"])
        cursor.execute("select * from Redemption_Details where `Bond Number` = %s",(str(a),))
        data=cursor.fetchall()
        cursor.execute("select * from Purchase_Details where `Bond Number` = %s",(str(a),))
        data2=cursor.fetchall()
        for i in range(len(data)):
            data[i]=data[i]+data2[i][1:4]+data2[i][6:]
        if len(data)==0:
            return render_template("notavailable.html")
        else:
             return render_template("base.html",column=c1,rows=data)

@app.route("/Q2",methods=["GET","POST"])
def Q2():
    if request.method=="POST":
        comp=request.form["buyer"]
        print(type(comp))
        cursor.execute("select Denominations from Purchase_Details where `Name of the Purchaser`=%s",(comp,))
        b=cursor.fetchall()
        cursor.execute("select `Date of Purchase` from Purchase_Details where `Name of the Purchaser`=%s",(comp,))
        c=cursor.fetchall()
        # print(c)
        if (len(b)!=0 and len(c)!=0):
            y19=0
            y20=0
            y21=0
            y22=0
            y23=0
            y24=0
            for i in range(len(b)):
                b[i]=(''.join(b[i])).replace(",", "")
            # print(b)
            for i in range(len(c)):
                if c[i][0][-2:]=='19':
                     y19+=int(b[i])
                elif c[i][0][-2:]=='20':
                     y20+=int(b[i])
                elif c[i][0][-2:]=='21':
                     y21+=int(b[i])
                elif c[i][0][-2:]=='22':
                     y22+=int(b[i])
                elif c[i][0][-2:]=='23':
                     y23+=int(b[i])
                elif c[i][0][-2:]=='24':
                     y24+=int(b[i])
            d=[y19,y20,y21,y22,y23,y24]
            e=['19','20','21','22','23','24']
            print(d)
            return render_template("Q2.html",money=d,year=e)
@app.route("/Q3",methods=["GET","POST"])
def Q3():
    if request.method=="POST":
        par=request.form["party"]
        cursor.execute("select Denominations from Redemption_Details where `Name of the Political Party`=%s",(par,))
        b=cursor.fetchall()
        cursor.execute("select `Date of Encashment` from Redemption_Details where `Name of the Political Party`=%s",(par,))
        c=cursor.fetchall()
        if (len(b)!=0 and len(c)!=0):
            y19=0
            y20=0
            y21=0
            y22=0
            y23=0
            y24=0
            for i in range(len(b)):
                b[i]=(''.join(b[i])).replace(",", "")
            # print(b)
            for i in range(len(c)):
                if c[i][0][-2:]=='19':
                     y19+=int(b[i])
                elif c[i][0][-2:]=='20':
                     y20+=int(b[i])
                elif c[i][0][-2:]=='21':
                     y21+=int(b[i])
                elif c[i][0][-2:]=='22':
                     y22+=int(b[i])
                elif c[i][0][-2:]=='23':
                     y23+=int(b[i])
                elif c[i][0][-2:]=='24':
                     y24+=int(b[i])
            d=[y19,y20,y21,y22,y23,y24]
            e=['19','20','21','22','23','24']
            # f=[y191,y201,y211,y221,y231,y241]
            return render_template("Q3.html",money=d,year=e)
@app.route("/Q4",methods=["GET","POST"])
def Q4():
    if request.method=="POST":
        par=request.form["party"]
        cursor.execute("Select Purchase_Details.Denominations,`Name of the Purchaser` from  Purchase_Details inner join Redemption_Details where Redemption_Details.`Bond Number`= Purchase_Details.`Bond Number` and Purchase_Details.Prefix = Redemption_Details.Prefix and Redemption_Details.`Name of the Political Party`=%s",(par,))
        cp=cursor.fetchall()
        l={}
        print(cp)
        if len(cp)==0:
            return render_template("notavailable.html")
        else:
            for i in cp:
                if i[1] not in l:
                   l[i[1]]=0
                l[i[1]]+=int(i[0].replace(",",""))
        k=[]
        m=[]
        n=0
        for i in l:
            k.append([i,l[i]])
            n+=l[i]
        return render_template("Q4.html",person=k,total=n)
@app.route("/Q5",methods=["GET","POST"])
def Q5():
        if request.method=="POST":
            buy=request.form["buyer"]
            cursor.execute("Select Redemption_Details.Denominations,`Name of the Political Party` from  Redemption_Details inner join Purchase_Details where Redemption_Details.`Bond Number`= Purchase_Details.`Bond Number` and Purchase_Details.Prefix = Redemption_Details.Prefix and Purchase_Details.`Name of the Purchaser`=%s",(buy,))
            cp=cursor.fetchall()
            l={}
            print(cp)
            if len(cp)==0:
                return render_template("notavailable.html")
            else:
                for i in cp:
                    if i[1] not in l:
                        l[i[1]]=0
                    l[i[1]]+=int(i[0].replace(",",""))
        k=[]
        m=[]
        print(l)
        print(sum(list(l.values())))
        n=0
        for i in l:
            k.append([i,l[i]])
            n+=l[i]
        return render_template("Q5.html",person=k,total=n)
@app.route("/Q6",methods=["GET","POST"])
def Q6():
    if request.method=="POST":
        z=[]
        z1=[]
        cursor.execute("select distinct `Name of the Political Party` from Redemption_Details")
        l=list(cursor.fetchall())

        for i in l:
            cursor.execute("Select Denominations from Redemption_Details where `Name of the Political Party`=%s",(i[0],))
            k=cursor.fetchall()
            sum=0
            for j in k:
                sum+=int(j[0].replace(",",""))
            z.append([i[0]])
            z1.append(sum)
        return render_template("Q6.html",data=z1,label=z)
@app.route("/Extra",methods=["GET","POST"])
def Extra():
            if request.method=="POST":
                 buy=request.form["buyer"]
            cursor.execute("Select Redemption_Details.Denominations,`Name of the Political Party` from  Redemption_Details inner join Purchase_Details where Redemption_Details.`Bond Number`= Purchase_Details.`Bond Number` and Purchase_Details.Prefix = Redemption_Details.Prefix and Purchase_Details.`Name of the Purchaser`=%s",(buy,))
            cp=cursor.fetchall()
            l={}
            print(cp)
            if len(cp)==0:
                return render_template("notavailable.html")
            else:
                for i in cp:
                    if i[1] not in l:
                        l[i[1]]=0
                    l[i[1]]+=int(i[0].replace(",",""))
            k=[]
            m=[]
            print(l)
            print(sum(list(l.values())))
            n=0
            for i in l:
                 k.append([i,l[i]])
                 m.append(l[i])
            return render_template("Extra.html",person=k,moneyall=m)    
        
    
        
if __name__== "__main__":
    app.run(debug=True)

    
    
    
# cursor.execute("Show columns from party")
# t=cursor.fetchall()
# for i in t:
#     print(i[0])