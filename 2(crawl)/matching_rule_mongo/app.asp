<%@LANGUAGE="VBSCRIPT" CODEPAGE="65001"%>
<%
Response.CodePage = 65001
Session.CodePage = 65001
Response.Charset = "utf-8"
%>
<!--#include virtual="/app/inc/Userchk.asp"-->
<!--#include virtual="/config/sqlconn.asp"-->
<!--#include virtual="/app/inc/func.asp"-->
<!--#include file="sqlconn.asp"-->
<!--#include file="func.asp"-->
<style>
*{line-height:26px;font-size:15px}
</style>
<%
'''##########
dim TID
RID = Trim(ReQuest("id"))
TID = Trim(ReQuest("tid"))

if isPint(RID)=false then RID=0

if isPint(TID)=false then TID=0

'''##########
DBS_ServIP = "192.168.1.33"
DBS_Name = "Crawl_Task"

'''##########
call sDbOpen("")

'''##########
On Error Resume Next

'''##########
dim Task_RID
dim sTxt

dim sTitle
dim sDescr
dim sKWS
dim sPath

'''##########
SqlCmd = "SELECT TOP 10 RID,Task_RID,Rule_URL,Rule_Match_C,Rule_Match_T,Rule_Match_D,Rule_Match_K,Rule_Match_P"
SqlCmd = SqlCmd & " FROM [dbo].[Crawl_Task_Rule]"
SqlCmd = SqlCmd & " where 1=1"
if TID<>0 then SqlCmd = SqlCmd & " and Task_RID="&TID&""
SqlCmd = SqlCmd & " and RID>"&RID&""
SqlCmd = SqlCmd & " Order by RID asc"
'Response.write "<br>SqlCmd = " & SqlCmd
Set Rs = sConn.ExeCute(SqlCmd)
If Not Rs.Eof Then
	Do while Not Rs.Eof
		sRID=Rs(0)
		sTID=Rs(1)
		sURL=Rs(2)
		sTxt=Rs(3)
		sTitle=Rs(4)
		sDescr=Rs(5)
		sKWS=Rs(6)
		sPath=Rs(7)
		
		Task_RID=sTID

		'Response.write sTxt
		'Response.write "<br/>Len(sTxt)=" & Len(sTxt)
		
		'''##########
		if isnull(sTxt) then sTxt=""
		
		'''##########
		'Response.write sTxt
		if sTxt<>"" then
			'''##########
			sTxt=filterTag_style(sTxt)
			sTxt=filterTag_class(sTxt)
			sTxt=filterTag_script(sTxt)
			sTxt=filterTag_style(sTxt)
			sTxt=filterTag_pics(sTxt)
			sTxt=filterTag_Misc(sTxt)
		
			'''##########
			sTxt=replace(sTxt, "<A", "<a")
			sTxt=replace(sTxt, "</A>", "</a>")

			if (instr(sTxt,"白癜风")>0 OR instr(sTxt,"牛皮癣")>0) OR (instr(sTxt,"价格")>0 And instr(sTxt,"多少")>0) OR instr(sTxt,"</br></br></br></br></br><a") then
				pos=instr(sTxt,"<BR><BR><BR><BR><BR><BR><a")
				if pos>0 then
					sTxt=left(sTxt, pos-1)
				end if
				'sTxt=filterTag_Href(sTxt)
				sTxt=filterTag_HealthAds(sTxt)
				
				if (instr(sTxt,"白癜风")>0 OR instr(sTxt,"牛皮癣")>0) then
					pos=instr(sTxt,"<a")
					if pos>0 then
						sTxt=left(sTxt, pos-1)
					end if
					'sTxt=filterTag_Href(sTxt)
					sTxt=filterTag_HealthAds(sTxt)

					'Response.write "<hr/><hr/><hr/><hr/>"& sTxt
					'Response.end
				end if
			end if

			'''##########
			sTxt=RegfilterByDB(sTxt,Task_RID,5,4)
			'Response.write "<br/>Len(sTxt)=" & Len(sTxt)

			'''##########
			sTxt=replace(sTxt, "（", "(")
			sTxt=replace(sTxt, "）", ")")
			sTxt=replace(sTxt, "：", ":")
			sTxt=replace(sTxt, "▲", "")
			sTxt=replace(sTxt, "▼", "")
			sTxt=replace(sTxt, "★", "")
			sTxt=replace(sTxt, "↓", "")
			sTxt=replace(sTxt, "↑", "")

			'Response.write "<hr/><hr/><hr/><hr/>"& sTxt
			'Response.end
			'''##########
			sTxt=replace(sTxt, "<P", "<p")
			sTxt=replace(sTxt, "</P>", "</p>")

			sTxt=replace(sTxt, "\u3000", "", 1,-1,1)
			sTxt=replace(sTxt, "\r", "", 1,-1,1)
			sTxt=replace(sTxt, "\t", "", 1,-1,1)

			sTxt=replace(sTxt, "<p\>", "<p>", 1,-1,1)
			sTxt=replace(sTxt, "<div", "<p", 1,-1,1)
			sTxt=replace(sTxt, "</div>", "</p>", 1,-1,1)

			sTxt=replace(sTxt, "<br>", "<br/>", 1,-1,1)
			sTxt=replace(sTxt, "</br>", "<br/>", 1,-1,1)
			sTxt=replace(sTxt, "<br />", "<br/>", 1,-1,1)

			sTxt=replace(sTxt, "	", " ", 1,-1,1)
			sTxt=replace(sTxt, "&nbsp;", " ", 1,-1,1)

			for i=1 to 10
				sTxt=replace(sTxt, "--", "-")
				sTxt=replace(sTxt, "==", "=")
				sTxt=replace(sTxt, "  ", " ", 1,-1,1)
				sTxt=replace(sTxt, "<br/><br/>", "<br/>", 1,-1,1)
			next
			sTxt=replace(sTxt, "> <", "><")

			'''##########
			sTxt=replace(sTxt, "<br/></p>", "</p>", 1,-1,1)
			sTxt=replace(sTxt, "<br/><p", "<p", 1,-1,1)
			sTxt=replace(sTxt, "<p><br/>", "<p>", 1,-1,1)
			sTxt=replace(sTxt, "<p>=</p>", "", 1,-1,1)
			sTxt=replace(sTxt, "<p>-</p>", "", 1,-1,1)
			sTxt=replace(sTxt, "<p></p>", "", 1,-1,1)
			
			'''##########
			for i=1 to 2
				sTxt=replace(sTxt, "<p><p><p>", "<p>", 1,-1,1)
				sTxt=replace(sTxt, "</p></p></p>", "</p>", 1,-1,1)

				sTxt=replace(sTxt, "<p><p>", "<p>", 1,-1,1)
				sTxt=replace(sTxt, "</p></p>", "</p>", 1,-1,1)
			next
			sTxt=replace(sTxt, "<p\>", "<p>", 1,-1,1)

			'''##########截取信息
			'''getSPAMSTR(任务编号,对应字段,规则类型)
			SPAM_STR = getSPAMSTR(Task_RID,5,2)
			'Ts1=Split(SPAM_STR, ",")
			Ts1=Split(SPAM_STR, vbcrlf)
			Ts2=Ubound(Ts1)
			'''##########
			For Ts3=0 to Ts2
				TEMP_STR = Ts1(Ts3)
				'''##########
				pos=instr(TEMP_STR, "|")
				if pos>0 then
					TEMP_STR_A=left(TEMP_STR,pos-1)
					TEMP_STR_B=mid(TEMP_STR,pos+1)
				else
					TEMP_STR_A=""
					TEMP_STR_B=""
				end if

				'''##########
				if isnull(TEMP_STR_A) then TEMP_STR_A=""
				if TEMP_STR_A<>"" then
					pos=instr(sTxt, TEMP_STR_A)
					if pos>0 then
						sTxt = mid(sTxt, pos)
					end if
				end if
				
				'''##########
				if isnull(TEMP_STR_B) then TEMP_STR_B=""
				if TEMP_STR_B<>"" then
					pos=instr(sTxt, TEMP_STR_B)
					if pos>0 then
						sTxt = left(sTxt, pos-1)
					end if
				end if
			Next
			
			'''##########替换信息
			'''getSPAMSTR(任务编号,对应字段,规则类型)
			SPAM_STR = getSPAMSTR(Task_RID,5,3)
			
			'''##########
			'Ts1=Split(SPAM_STR, ",")
			Ts1=Split(SPAM_STR, vbcrlf)
			Ts2=Ubound(Ts1)

			'''##########
			For Ts3=0 to Ts2
				TEMP_STR = Ts1(Ts3)
				'''##########
				pos=instr(TEMP_STR, "|")
				if pos>0 then
					TEMP_STR_A=left(TEMP_STR,pos-1)
					TEMP_STR_B=mid(TEMP_STR,pos+1)
				else
					TEMP_STR_A=""
					TEMP_STR_B=""
				end if

				'''##########
				if isnull(TEMP_STR_A) then TEMP_STR_A=""
				if isnull(TEMP_STR_B) then TEMP_STR_B=""

				if TEMP_STR_A<>"" then
					sTxt=replace(sTxt, TEMP_STR_A, TEMP_STR_B, 1, -1, 1)
				end if
			Next
			
			'''##########某些字符多次出现，则信息置空，作废
			SPAM_STR = "?"
			SPAM_STR = SPAM_STR & ",!"
			'SPAM_STR = SPAM_STR & ",<p>"
			
			'''##########
			Ts1=Split(SPAM_STR, ",")
			Ts2=Ubound(Ts1)
			'''##########
			For Ts3=0 to Ts2
				TEMP_STR = Ts1(Ts3)
				pos=instr(sTxt, TEMP_STR)
				if pos>0 then
					Total_Times=Ubound(Split(sTxt, TEMP_STR))
					if Total_Times>20 then sTxt="检测出垃圾信息, 含有 "&TEMP_STR&" 字符太多."
				end if
			Next
			
			'''##########
			sTxt=RegfilterByDB(sTxt,Task_RID,5,4)
			
			'''##########
			sLen=Len(sTxt)
			
			'''##########
			p_tag_1="<p"
			p_tag_2="</p>"

			'''##########
			Ts1=Split(sTxt, p_tag_2)
			Ts2=Ubound(Ts1)
			'''##########
			if Ts2<3 and sLen>300 then
				sTxt = replace(sTxt, "。", "。</p><p>")
			end if
			
			'''##########
			p_tag_1="<table"
			p_tag_2="</table>"
			pos1=Instr(1,sTxt,p_tag_1,1)
			pos2=Instr(1,sTxt,p_tag_2,1)
			if pos1>0 and pos2=0 Then
				sTxt=sTxt & "</table>"
			elseif pos1=0 and pos2>0 Then
				sTxt="<table>" & sTxt
			end if
			
			'''##########
			Ts1=Ubound(Split(sTxt, "<a"))
			Ts2=Ubound(Split(sTxt, "</a>"))
			'''##########
			if Ts1<>Ts2 then
				sTxt=filterTag_Href(sTxt)
			end if
			
			'''##########
			Ts1=Ubound(Split(sTxt, "<strong"))
			Ts2=Ubound(Split(sTxt, "</strong>"))
			'''##########
			if Ts1<>Ts2 then
				sTxt=filterTag_strong(sTxt)
			end if

			p_tag_1="<a"
			p_tag_2="</a>"
			pos1=InstrRev(sTxt,p_tag_1,-1,1)
			pos2=InstrRev(sTxt,p_tag_2,-1,1)
			if pos1>0 and pos2=0 Then
				sTxt=sTxt & "</a>"
			elseif pos1=0 and pos2>0 Then
				sTxt="<a name=""#"">" & sTxt
			elseif pos1>pos2 and pos2>0 Then
				sTxt=sTxt & "</a>"
			end if
			
			'''##########
			p_tag_1="<p"
			p_tag_2="</p>"
			pos1=Instr(1,sTxt,p_tag_1,1)
			pos2=Instr(1,sTxt,p_tag_2,1)

			if pos1>0 OR pos2>0 Then
				if pos1>pos2 and pos2>0 then sTxt="<p>" & sTxt

				pos1=InstrRev(sTxt,p_tag_1,-1,1)
				pos2=InstrRev(sTxt,p_tag_2,-1,1)
				
				'Response.write vbcrlf & vbcrlf & "<hr/><span class=""proj"">pos1=</span></hr>" & pos1
				'Response.write vbcrlf & vbcrlf & "<hr/><span class=""proj"">pos2=</span></hr>" & pos2

				if pos1>pos2 then sTxt=sTxt & "</p>"
				
				s3=Split(sTxt, p_tag_1, -1, 1)
				HTML_cntA=Ubound(s3)

				s4=Split(sTxt, p_tag_2, -1, 1)
				HTML_cntB=Ubound(s4)

				if HTML_cntA<>HTML_cntB then
					if HTML_cntA>HTML_cntB then
						for p_i=1 to (HTML_cntA-HTML_cntB)
							sTxt=sTxt & "</p>"
						Next
					else
						for p_i=1 to (HTML_cntB-HTML_cntA)
							sTxt="<p>"&sTxt
						Next
					end if
				end if
			end if
			
			'''##########
			for i=1 to 2
				sTxt=replace(sTxt, "<br/><p>", "<p>", 1, -1, 1)
				sTxt=replace(sTxt, "<br/></p>", "</p>", 1, -1, 1)

				sTxt=replace(sTxt, "<p><br/>", "<p>", 1, -1, 1)
				sTxt=replace(sTxt, "</p><br/>", "</p>", 1, -1, 1)
				sTxt=replace(sTxt, "<p>:</p>", "", 1, -1, 1)
				sTxt=replace(sTxt, "<p></p>", "", 1, -1, 1)
			Next
			sTxt=replace(sTxt, "> <", "><", 1, -1, 1)

			if instr(sTxt,"”")>0 then
				sTxt=replace(sTxt, "<p>”<br/>", "<p>”", 1, -1, 1)
				sTxt=replace(sTxt, "<p>“<br/>", "<p>“", 1, -1, 1)
				sTxt=replace(sTxt, "</p><p>”", "”</p><p>", 1, -1, 1)
			end if
			
			'''##########
			sLen=Len(LoseHTML(sTxt))
			
			if sLen<200 then
				sTxt=""
			end if
		end if

		'''##########
		call filter_title()

		'''##########
		call filter_Descr()

		'''##########
		'Response.write "<br/><b>Path</b>=" & sPath
		call filter_Path()

		'''##########
		Response.write "<hr/>" & vbcrlf & vbcrlf
		Response.write "<b>sRID</b>=" & sRID
		Response.write " ~~~ <b>Len</b>=" & sLen
		Response.write " ~~~ <b>url</b>=<a target=""_blank"" href="""& sURL &""">" & sURL & "</a>"
		Response.write "<br/><b>Title</b>=" & sTitle
		Response.write "<br/><b>Description</b>=" & sDescr
		Response.write "<br/><b>Keywords</b>=" & sKWS
		Response.write "<br/><b>Path</b>=" & sPath
		Response.write "<br/>------<br/>" & vbcrlf & vbcrlf
		Response.write sTxt
		
		Response.write vbcrlf & vbcrlf

		'''##########
		'sTxt=replace(sTxt, "'", "''")
		'SqlCmd = "update [Crawl_Task_Rule] set [Rule_Match_C]=N'"&sTxt&"' where RID="&RID&""
		'sConn.ExeCute(SqlCmd)

		if 1=2 then
			SqlCmd = "select top 1 * from [Crawl_Task_Rule] where RID=" & sRID & ""
			'Response.write "<br>SqlCmd = " & SqlCmd
			Set RU=server.createobject("adodb.recordset")
			RU.open SqlCmd, sConn, 1, 3

			RU("Rule_Match_C")=sTxt

			RU.update
			RU.Close
			Set RU=Nothing
		end if
	Rs.MoVeNext
	Loop
End if
Set Rs=Nothing

'''##########
Call sDbClose("conn")

'''##########
'NextLink = Get_CurrPage()
NextLink = "?tid=" & TID & "&id=" & sRID
Response.write vbcrlf
Response.write "<br/><a href="""&NextLink&""">" & NextLink & "</a>"
Response.write vbcrlf
'Response.Redirect NextLink
'Response.End

Alert_msg = "更新成功..."
Response.write "<script type=""text/javascript"">" & vbcrlf
Response.write "<!--" & vbcrlf
'Response.write "window.alert('" & Alert_msg & "');"
'Response.write "window.location.href='" & NextLink & "';" & vbcrlf
'Response.write "window.opener.location.reload();" & vbcrlf
'Response.write "window.close();" & vbcrlf
Response.write "//-->" & vbcrlf
Response.write "</script>"
%>
