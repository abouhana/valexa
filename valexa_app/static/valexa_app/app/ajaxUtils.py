
from JS import JSON, XMLHttpRequest, decodeURIComponent, document, encodeURIComponent, typeof, Object, ActiveXObject #__: skip
from transcrypt import __new__, __pragma__ #__: skip

__pragma__('js', '{}', """
if (!Object.entries) {
    Object.entries = function( obj ){
        var ownProps = Object.keys( obj ),
            i = ownProps.length,
            resArray = new Array(i);
        while (i--)
        resArray[i] = [ownProps[i], obj[ownProps[i]]];
        
        return resArray;
    };
}""")

__pragma__('js', '{}', """//IE polyfill""")
if typeof(HTMLCollection.prototype[Symbol.iterator]) is "undefined":
    HTMLCollection.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator]
    HTMLFormControlsCollection.prototype[Symbol.iterator] = Array.prototype[Symbol.iterator]

DEFAULT_MESSAGES_ID = 'django_messages'

def handleMessages(data, messages_id=DEFAULT_MESSAGES_ID):
    msgs = getattr(data, messages_id, [])
    if len(msgs) > 0:
        msg_div = document.getElementById(messages_id)
        msg_elem = msg_div.querySelector('.alert')
        msg_div.innerHTML = ""
        for msg in msgs:
            msg_node = msg_elem.cloneNode()
            msg_node.className = "alert"
            msg_node.classList.add(msg.tags)
            msg_node.innerHTML = msg.text
            msg_div.appendChild(msg_node)

        msg_div.style.removeProperty('display') 

__pragma__('noalias', 'type')
__pragma__('noalias', 'name')


def ajax(param):
    """
    XMLHttpRequest interface based on jQuery.ajax
    >>> ajax({
        type: type,
        url: url,
        data: data,
        success: function(){},
        error: function(){},
        contentType: contentType,
        dataType: dataType,
        headers: { header1Name: header1Content },
        beforeSend: function(){},
    })
    """
    if window.XMLHttpRequest:
        xhr = __new__(XMLHttpRequest)()
    else:
        xhr = __new__(ActiveXObject("Microsoft.XMLHTTP"))()
    
    xhr.open(param.type, param.url)

    if param.contentType:
       content_type = param.contentType
    else:
        content_type = "application/x-www-form-urlencoded; charset=UTF-8"

    if param.dataType:
        xhr.responseType = param.dataType
    
    xhr.setRequestHeader('Content-Type', content_type)

    xhr.setRequestHeader('X-Requested-With', 'XMLHttpRequest')
    if param.headers:
        for header,value in Object.entries(param.headers):
            xhr.setRequestHeader(header, value)

    def xhr_onload():
        if xhr.status is 200:
            try:
                param.success(JSON.parse(xhr.responseText), xhr.statusText, xhr)
            except:
                param.success(xhr.responseText, xhr.statusText, xhr)
        else:
            if param.error:
                param.error(xhr, xhr.statusText, xhr.responseText)
            else:
                alert("ajax response error: "+xhr.responseText)

    xhr.onload = xhr_onload
    xhr.onerror = lambda x, y, z: param.error(xhr, xhr.statusText, "Unknown Error Occured. Server response not received.")
    if param.beforeSend:
        param.beforeSend(xhr, param)

    if param.data:
        xhr.send(param.data)
    else:
        xhr.send()

def serialize(obj):
    s = []
    for key,value in Object.entries(obj):
        s.append(encodeURIComponent(key) + "=" + encodeURIComponent(value))
    return ("&".join(s)).replace('/%20/', '+')    

def formSerialize(form):
    s = [] #__: jsiter
    if typeof(form) == 'object' and form.nodeName.toLowerCase() == 'form':
        for field in form.elements:
            if field.name and not field.disabled and field.type not in ['file', 'reset', 'submit', 'button']:
                if field.type == 'select-multiple':
                    for option in reversed(field.options):
                        if option.selected:
                            s[s.length] = encodeURIComponent(field.name) + "=" + encodeURIComponent(field.options[j].value)
                elif field.type not in ['checkbox', 'radio'] or field.checked:
                    s[s.length] = encodeURIComponent(field.name) + "=" + encodeURIComponent(field.value)
    return ("&".join(s)).replace('/%20/', '+')

def formJSON(form):
    s = {} #__: jsiter
    if typeof(form) == 'object' and form.nodeName.toLowerCase() == 'form':
        for field in form.elements:
            if field.name and not field.disabled and field.type not in ['file', 'reset', 'submit', 'button']:
                if field.type == 'select-multiple':
                    s[field.name] = []
                    for option in reversed(field.options):
                        if option.selected:
                            s[field.name].append(option.value)
                elif field.type not in ['checkbox', 'radio']:
                    s[field.name] = field.value
                elif field.checked:
                    if not s[field.name]:
                        s[field.name] = field.value
                    elif type(s[field.name]) is not list:
                        s[field.name] = [s[field.name]]
                        s[field.name].append(field.value)
                    else:
                        s[field.name].append(field.value)

    return JSON.stringify(s)

__pragma__('alias', 'name', 'py_name')
__pragma__('alias', 'type', 'py_type')


def csrfCompat(xhr, settings):
    if not csrfSafeMethod(settings.type) and sameOrigin(settings.url):
        # Send the token to same-origin, relative URLs only.
        # Send the token only if the method warrants CSRF protection
        # Using the CSRFToken value acquired earlier
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'))


def getCookie(cookie_name):
    cookie_value = None
    if document.cookie and document.cookie is not '':
        cookies = document.cookie.js_split(';')
        for cookie in cookies:
            cookie = cookie.strip()
            if cookie[:len(cookie_name)+1] == cookie_name+'=':
                cookie_value = decodeURIComponent(cookie[len(cookie_name)+1:])
                break
    return cookie_value


def csrfSafeMethod(method):
    return ("/^(GET|HEAD|OPTIONS|TRACE)$/".test(method))

def sameOrigin(url):
    # test that a given url is a same-origin URL
    # url could be relative or scheme relative or absolute
    host = document.location.host # host + port
    protocol = document.location.protocol
    sr_origin = '//' + host
    origin = protocol + sr_origin
    # Allow absolute or scheme relative URLs to same origin or any other URL 
    # that isn't scheme relative or absolute i.e relative.
    return (
        (url == origin or url.slice(0, origin.length + 1) == origin + '/')
        or
        (url == sr_origin or url.slice(0, sr_origin.length + 1) == sr_origin + '/')
        or
        not "/^(\/\/|http:|https:).*/".test(url)
    )
        