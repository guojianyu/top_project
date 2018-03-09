<%
'''##########
sub filter_title()
	sTitle = getTDKSTR(sTitle)
	
	'''##########替换信息
	'''getSPAMSTR(任务编号,对应字段,规则类型)
	SPAM_STR = getSPAMSTR(Task_RID,1,3)
	
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
			sTitle=replace(sTitle, TEMP_STR_A, TEMP_STR_B, 1, -1, 1)
		end if
	Next
end sub

'''##########
sub filter_Descr()
	sDescr = getTDKSTR(sDescr)
	sDescr = Left(sDescr,300)
end sub

'''##########
sub filter_Path()
if sPath<>"" then
	'''##########替换信息
	'''getSPAMSTR(任务编号,对应字段,规则类型)
	SPAM_STR = getSPAMSTR(Task_RID,4,3)
	
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
			sPath=replace(sPath, TEMP_STR_A, TEMP_STR_B, 1, -1, 1)
		end if
	Next

	sPath = getTDKSTR(sPath)
	sPath = replace(sPath," ","")
	'sPath = replace(sPath,"当前位置","")
	'sPath = replace(sPath,":","")
	'sPath = replace(sPath,"：","")
	'sPath = replace(sPath,"首页>","")
	sPath = replace(sPath,"&gt;",">", 1, -1, 1)
	sPath = replace(sPath,"&nbsp;",">", 1, -1, 1)
	sPath = replace(sPath,"->",">")
	sPath = replace(sPath,">>>",">")
	sPath = replace(sPath,">>",">")
	
	sPath = replace(sPath,"分享到","")
	sPath = replace(sPath,">正文","")
	sPath = replace(sPath,"正文","")
	
	sPath_TMP = sPath
	sTitle_TMP = sTitle
	pos = instr(PathTagformat(sPath_TMP), PathTagformat(sTitle_TMP))
	if pos>0 then
		pos = instrRev(sPath, ">")
		if pos>0 then sPath = left(sPath, pos-1)
	end if

	sPath = trim(sPath)
	sPath = PathTagformat(sPath)
	if right(sPath,1)=">" then sPath=left(sPath,Len(sPath)-1)
	if left(sPath,1)=">" then sPath=mid(sPath,2)

end if
end sub

'''##########
Function PathTagformat(TMP_STR)
strng=TMP_STR
if isnull(strng) then strng=""
if strng<>"" then
	strng=replace(strng,"&quot;","")

	Dim regEx, Match, Matches ' 建立变量
	Set regEx = New RegExp ' 建立正则表达式
	'regEx.Pattern = patrn ' 设置模式
	'regEx.Pattern = "[\u4E00-\u9FA5]*"
	regEx.Pattern = "[a-zA-Z\u4E00-\u9FA5\d+\-\>]"
	'regEx.Pattern = "(\d+)"
	regEx.IgnoreCase = True ' 设置是否区分字符大小写
	regEx.Global = True ' 设置全局可用性
	Set Matches = regEx.Execute(strng) ' 执行搜索
	For Each Match in Matches ' 遍历匹配集合
		'RetStr = RetStr & "Match found at position "
		'RetStr = RetStr & Match.FirstIndex & ". Match Value is '"
		RetStr = RetStr & Match.Value
	Next
	PathTagformat = RetStr
end if
End Function

'''##########
Function getTDKSTR(TMPSTR)
	TMP_STR=TMPSTR
	if isnull(TMP_STR) then TMP_STR=""
	if TMP_STR<>"" then
		TMP_STR=replace(TMP_STR, "（", "(")
		TMP_STR=replace(TMP_STR, "）", ")")
		TMP_STR=replace(TMP_STR, "：", ":")
		TMP_STR=replace(TMP_STR, "▲", "")
		TMP_STR=replace(TMP_STR, "▼", "")
		TMP_STR=replace(TMP_STR, "★", "")
		TMP_STR=replace(TMP_STR, "↓", "")
		TMP_STR=replace(TMP_STR, "↑", "")
		TMP_STR=replace(TMP_STR, "【", "")
		TMP_STR=replace(TMP_STR, "】", "")
		TMP_STR=replace(TMP_STR, "\u3000", "", 1,-1,1)
		TMP_STR=replace(TMP_STR, "\r", "", 1,-1,1)
		TMP_STR=replace(TMP_STR, "\t", "", 1,-1,1)
	end if
	getTDKSTR=TMP_STR
end Function

'''##########
Function RegfilterByDB(TMPSTR,TMP_TaskID,TMP_fld,TMP_Type)
	'''##########
	'''getSPAMSTR(任务编号,对应字段,规则类型)
	'''##########
	SqlCmd = "select Task_Txt"
	SqlCmd = SqlCmd & " from [Crawl_Data_Format]"
	SqlCmd = SqlCmd & " where isDelete=0"
	SqlCmd = SqlCmd & " And Task_ID in(0," & TMP_TaskID & ")"
	SqlCmd = SqlCmd & " And Task_fld in(0," & TMP_fld & ")"
	SqlCmd = SqlCmd & " And Task_Type in(0," & TMP_Type & ")"
	'response.write "<br/>SqlCmd=" & SqlCmd
	Set Rs_spam = sConn.ExeCute(SqlCmd)
	If Not Rs_spam.Eof Then
		
		Dim TMP_STR,regEx
		TMP_STR=Cstr(TMPSTR)
		Set regEx=New RegExp
		regEx.IgnoreCase=True
		regEx.Global=True

		Do while Not Rs_spam.Eof
			Rule_STR=Rs_spam(0)
			if isnull(Rule_STR) then Rule_STR=""
			'if Rule_STR<>"" then Rule_STR=replace(Rule_STR,vbcrlf,"")
			
			'''##########
			'Ts1=Split(Rule_STR, ",")
			Ts1=Split(Rule_STR, vbcrlf)
			Ts2=Ubound(Ts1)

			'''##########
			For Ts3=0 to Ts2
				spam_STR = Ts1(Ts3)
				'''##########
				pos=instr(spam_STR, "|")
				if pos>0 then
					TEMP_STR_A=left(spam_STR,pos-1)
					TEMP_STR_B=mid(spam_STR,pos+1)
				else
					TEMP_STR_A=""
					TEMP_STR_B=""
				end if

				'''##########
				if isnull(TEMP_STR_A) then TEMP_STR_A=""
				if isnull(TEMP_STR_B) then TEMP_STR_B=""

				if TEMP_STR_A<>"" then
					regEx.Pattern=TEMP_STR_A
					TMP_STR=regEx.Replace(TMP_STR, TEMP_STR_B)
				end if
			Next
			
		Rs_spam.MoVeNext
		Loop

		RegfilterByDB=TMP_STR
		Set regEx=Nothing
	else
		RegfilterByDB=TMPSTR
	End if
	Set Rs_spam=Nothing
end Function

'''##########
Function getSPAMSTR(TMP_TaskID,TMP_fld,TMP_Type)
	'''##########
	SqlCmd = "select Task_Txt"
	SqlCmd = SqlCmd & " from [Crawl_Data_Format]"
	SqlCmd = SqlCmd & " where isDelete=0"
	SqlCmd = SqlCmd & " And Task_ID in(0," & TMP_TaskID & ")"
	SqlCmd = SqlCmd & " And Task_fld in(0," & TMP_fld & ")"
	SqlCmd = SqlCmd & " And Task_Type in(0," & TMP_Type & ")"
	'response.write "<br/>SqlCmd=" & SqlCmd
	Set Rs_spam = sConn.ExeCute(SqlCmd)
	If Not Rs_spam.Eof Then
		Do while Not Rs_spam.Eof
			Rule_STR=Rs_spam(0)
			if isnull(Rule_STR) then Rule_STR=""
			'if Rule_STR<>"" then Rule_STR=replace(Rule_STR,vbcrlf,"")
		Rs_spam.MoVeNext
		Loop
	else
		Rule_STR=""
	End if
	Set Rs_spam=Nothing
	getSPAMSTR=Rule_STR
End Function

'''##########
Function filterTag_HealthAds(TMPSTR)
	Dim TMP_STR,regEx
	TMP_STR=Cstr(TMPSTR)
	Set regEx=New RegExp
	regEx.IgnoreCase=True
	regEx.Global=True

	regEx.Pattern="\<a[\s\S]*?\<\/a\>"
	TMP_STR=regEx.Replace(TMP_STR,"")

	filterTag_HealthAds=TMP_STR

	Set regEx=Nothing
End Function

'''##########
Function filterTag_Source(TMPSTR)
	Dim TMP_STR,regEx
	TMP_STR=Cstr(TMPSTR)
	Set regEx=New RegExp
	regEx.IgnoreCase=True
	regEx.Global=True

	regEx.Pattern="\<p\>\(来源[\s\S]*?\)\<\/p\>"
	TMP_STR=regEx.Replace(TMP_STR,"")
	
	regEx.Pattern="\<p\>文章来源[\s\S]*?\</p\>"
	TMP_STR=regEx.Replace(TMP_STR,"")

	regEx.Pattern="\<p\>图片来源[\s\S]*?\</p\>"
	TMP_STR=regEx.Replace(TMP_STR,"")
	
	regEx.Pattern="\<p\>Related\ posts:\<ol\>\<li\>[\s\S]*?\<\/ol\>\<\/p\>"
	TMP_STR=regEx.Replace(TMP_STR,"")

	filterTag_Source=TMP_STR

	Set regEx=Nothing
End Function

'''##########
Function filterTag_editor(TMPSTR)
	Dim TMP_STR,regEx
	TMP_STR=Cstr(TMPSTR)
	Set regEx=New RegExp
	regEx.IgnoreCase=True
	regEx.Global=True

	regEx.Pattern="\<p\>本刊负责人[\s\S]*?\</p\>"
	TMP_STR=regEx.Replace(TMP_STR,"")
	
	regEx.Pattern="\<p\>作者[\s\S]*?\</p\>"
	TMP_STR=regEx.Replace(TMP_STR,"")
	
	regEx.Pattern="\<p\>简介[\s\S]*?\</p\>"
	TMP_STR=regEx.Replace(TMP_STR,"")

	filterTag_editor=TMP_STR

	Set regEx=Nothing
End Function

'''##########
Function filterTag_free(TMPSTR)
	Dim TMP_STR,regEx
	TMP_STR=Cstr(TMPSTR)
	Set regEx=New RegExp
	regEx.IgnoreCase=True
	regEx.Global=True

	regEx.Pattern="点击[\s\S]*?订阅"
	TMP_STR=regEx.Replace(TMP_STR,"")

	filterTag_free=TMP_STR

	Set regEx=Nothing
End Function

'''##########
Function filterTag_Href(TMPSTR)
	Dim TMP_STR,regEx
	TMP_STR=Cstr(TMPSTR)
	Set regEx=New RegExp
	regEx.Pattern="<(\/){0,1}a[^<>]*>"
	regEx.IgnoreCase=True
	regEx.Global=True
	TMP_STR=regEx.Replace(TMP_STR,"")
	filterTag_Href=TMP_STR
	Set regEx=Nothing
End Function

Function filterTag_strong(TMPSTR)
	Dim TMP_STR,regEx
	TMP_STR=Cstr(TMPSTR)
	Set regEx=New RegExp
	regEx.Pattern="<(\/){0,1}strong[^<>]*>"
	regEx.IgnoreCase=True
	regEx.Global=True
	TMP_STR=regEx.Replace(TMP_STR,"")
	filterTag_strong=TMP_STR
	Set regEx=Nothing
End Function

Function filterTag_DIV(ConStr)
	Dim tmpReStr, regEx
	tmpReStr = CStr(ConStr)
	Set regEx = New RegExp
	regEx.Pattern="<(\/){0,1}div[^<>]*>"
	regEx.IgnoreCase = True
	regEx.Global = True
	tmpReStr = regEx.Replace(tmpReStr, "")
	filterTag_DIV = tmpReStr
	Set regEx = Nothing
End Function

Function filterTag_class(ConStr)
	Dim tmpReStr, regEx
	tmpReStr = CStr(ConStr)
	Set regEx = New RegExp
	regEx.Pattern="\ class=\""[^\""]*\"""
	regEx.IgnoreCase = True
	regEx.Global = True
	tmpReStr = regEx.Replace(tmpReStr, "")
	filterTag_class = tmpReStr
	Set regEx = Nothing
End Function

Function filterTag_script(ConStr)
	Dim tmpReStr, regEx
	tmpReStr = CStr(ConStr)
	Set regEx = New RegExp
	regEx.IgnoreCase = True
	regEx.Global = True

	regEx.Pattern="\<script[\s\S]*?\<\/script\>"
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="\<noscript[\s\S]*?\<\/noscript\>"
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="\ onload=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\ onmouseout=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\ onmouseover=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\ onclick=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	filterTag_script = tmpReStr
	Set regEx = Nothing
End Function

Function filterTag_style(ConStr)
	Dim tmpReStr, regEx
	tmpReStr = CStr(ConStr)
	Set regEx = New RegExp
	regEx.IgnoreCase = True
	regEx.Global = True

	regEx.Pattern="\<style[\s\S]*?\<\/style\>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\ style=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")

	filterTag_style = tmpReStr
	Set regEx = Nothing
End Function

Function filterTag_table(ConStr)
	Dim tmpReStr, regEx
	tmpReStr = CStr(ConStr)
	Set regEx = New RegExp
	regEx.IgnoreCase = True
	regEx.Global = True

	'regEx.Pattern="<table[\s\S]*?</table>"
	regEx.Pattern="<(\/){0,1}table[^<>]*>"
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="<(\/){0,1}th[^<>]*>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="<(\/){0,1}tr[^<>]*>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="<(\/){0,1}td[^<>]*>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="<(\/){0,1}tbody[^<>]*>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	filterTag_table = tmpReStr
	Set regEx = Nothing
End Function

Function filterTag_img(ConStr)
	Dim tmpReStr, regEx
	tmpReStr = CStr(ConStr)
	Set regEx = New RegExp
	regEx.IgnoreCase = True
	regEx.Global = True

	regEx.Pattern="\<img[\s\S]*?\>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	filterTag_img = tmpReStr
	Set regEx = Nothing
End Function

Function filterTag_DLDTDD(ConStr)
	Dim tmpReStr, regEx
	tmpReStr = CStr(ConStr)
	Set regEx = New RegExp
	regEx.IgnoreCase = True
	regEx.Global = True

	'regEx.Pattern="<table[\s\S]*?</table>"
	regEx.Pattern="<(\/){0,1}dl[^<>]*>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="<(\/){0,1}dt[^<>]*>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="<(\/){0,1}dd[^<>]*>"
	tmpReStr = regEx.Replace(tmpReStr, "")

	filterTag_DLDTDD = tmpReStr
	Set regEx = Nothing
End Function

Function filterTag_Misc(TMP_STR)
	Dim tmpReStr, regEx
	tmpReStr = trim(TMP_STR)
	Set regEx = New RegExp
	regEx.IgnoreCase = True
	regEx.Global = True

	regEx.Pattern="\ width=\'[^\']*\'"
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="\<style[\s\S]*?\<\/style\>"
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="\ data-cke-saved-src=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="\ align=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\ cellspacing=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\ cellpadding=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="\ border=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\ target=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="\<script[\s\S]*?\<\/script\>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	SPAM_STR="div,font,span,iframe,em"
	'SPAM_STR=SPAM_STR&","

	Ts1=Split(SPAM_STR, ",")
	Ts2=Ubound(Ts1)
	'''##########
	For Ts3=0 to Ts2
		TEMP_STR = Ts1(Ts3)
		regEx.Pattern="<(\/){0,1}"&TEMP_STR&"[^<>]*>"
		tmpReStr=regEx.Replace(tmpReStr, "")
	next

	''spam check
	'SPAM_STR=GetRPList(52)
	SPAM_STR=""

	Ts1=Split(SPAM_STR, ",")
	Ts2=Ubound(Ts1)
	'''##########
	For Ts3=0 to Ts2
		TEMP_STR = Ts1(Ts3)
		regEx.Pattern="\ "&TEMP_STR&"=\""[^\""]*\"""
		tmpReStr = regEx.Replace(tmpReStr, "")
		
		regEx.Pattern="\ "&TEMP_STR&"=\'[^\']*\'"
		tmpReStr = regEx.Replace(tmpReStr, "")
	next

	regEx.Pattern="\ href=\""javascript[\s\S]*?\"""
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\ target=\'\_blank\'"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\ data-href=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, " href=""http://")

	regEx.Pattern="\ class=[\s\S]*?>"
	tmpReStr = regEx.Replace(tmpReStr, ">")

	regEx.Pattern="\<a\ href=\""[^\""]*\""\>\<\/a\>"
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="\<a\ href=\""[\s\S]*?\""\>回顶部\<\/a\>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\<a\ href=\""[^\""]*\""\ \>回顶部\<\/a\>"
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="\<p\>发布日期：[\s\S]*?\<\/p\>"
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	filterTag_Misc = tmpReStr
	Set regEx = Nothing
End Function

Function filterTag_pics(TMP_STR)
	Dim tmpReStr, regEx
	tmpReStr = trim(TMP_STR)
	Set regEx = New RegExp
	regEx.IgnoreCase = True
	regEx.Global = True
	
	regEx.Pattern="\ alt=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")

	regEx.Pattern="\ width=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")
	
	regEx.Pattern="\ height=\""[^\""]*\"""
	tmpReStr = regEx.Replace(tmpReStr, "")

	filterTag_pics = tmpReStr
	Set regEx = Nothing
End Function

Function filterTag_H_Tag(TMP_STR)
	Dim tmpReStr, regEx
	tmpReStr = trim(TMP_STR)
	Set regEx = New RegExp
	regEx.IgnoreCase = True
	regEx.Global = True
	
	regEx.Pattern="\<h1\ [\s\S]*?\>"
	tmpReStr = regEx.Replace(tmpReStr, "<h1>")
	
	regEx.Pattern="\<h2\ [\s\S]*?\>"
	tmpReStr = regEx.Replace(tmpReStr, "<h2>")

	filterTag_H_Tag = tmpReStr
	Set regEx = Nothing
End Function
%>