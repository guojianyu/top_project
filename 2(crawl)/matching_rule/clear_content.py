from bs4 import BeautifulSoup
import re
def clear_content(content):
    per = re.compile('class=\S.*?[\'"]|id=\S.*?[\'"]|style=\S.*?[\'"]')#去除class id style
    content = re.sub(per, '', content)
    content = content.replace("（", "(")
    content =  content.replace("）", ")")
    content=  content.replace("：", ":")
    content = content.replace("▲", "")
    content = content.replace("▼", "")
    content = content.replace("★", "")
    content = content.replace("↓", "")
    content = content.replace("↑", "")
    content = content.replace("<P", "<p")
    content = content.replace("</P>", "</p>")
    content = content.replace("\u3000", "")
    content = content.replace("\r", "")
    content = content.replace("\t", "")
    content = content.replace( "<p\>", "<p>")
    content = content.replace("<div", "<p")
    content = content.replace("</div>", "</p>")
    content = content.replace( "<br>", "<br/>")
    content = content.replace("</br>", "<br/>")
    content = content.replace("<br />", "<br/>")
    content = content.replace( "	", " ")
    content = content.replace( "&nbsp;", " ")
    content = content.replace("<b>","<strong>")
    content = content.replace("</b>","</strong>")

    return content

def fix_html(markup):
    soup = BeautifulSoup(markup, 'lxml')
    fixed_html = soup.prettify().replace('<html>','').replace('<body>','')
    fixed_html = fixed_html.replace('</html>','').replace('</body>','')
    return fixed_html.strip()

if __name__ == "__main__":
    content = "<b class='ssssss'><!--This will be used in the crawler--></b></b>dddddd</b><p>It's wonderful"
    html = fix_html(content)
    ret = clear_content(html)
    print (ret)



