// Transcrypt'ed from Python, 2019-08-06 15:12:06
import {AssertionError, AttributeError, BaseException, DeprecationWarning, Exception, IndexError, IterableError, KeyError, NotImplementedError, RuntimeWarning, StopIteration, UserWarning, ValueError, Warning, __JsIterator__, __PyIterator__, __Terminal__, __add__, __and__, __call__, __class__, __envir__, __eq__, __floordiv__, __ge__, __get__, __getcm__, __getitem__, __getslice__, __getsm__, __gt__, __i__, __iadd__, __iand__, __idiv__, __ijsmod__, __ilshift__, __imatmul__, __imod__, __imul__, __in__, __init__, __ior__, __ipow__, __irshift__, __isub__, __ixor__, __jsUsePyNext__, __jsmod__, __k__, __kwargtrans__, __le__, __lshift__, __lt__, __matmul__, __mergefields__, __mergekwargtrans__, __mod__, __mul__, __ne__, __neg__, __nest__, __or__, __pow__, __pragma__, __proxy__, __pyUseJsNext__, __rshift__, __setitem__, __setproperty__, __setslice__, __sort__, __specialattrib__, __sub__, __super__, __t__, __terminal__, __truediv__, __withblock__, __xor__, abs, all, any, assert, bool, bytearray, bytes, callable, chr, copy, deepcopy, delattr, dict, dir, divmod, enumerate, filter, float, getattr, hasattr, input, int, isinstance, issubclass, len, list, map, max, min, object, ord, pow, print, property, py_TypeError, py_iter, py_metatype, py_next, py_reversed, py_typeof, range, repr, round, set, setattr, sorted, str, sum, tuple, zip} from './org.transcrypt.__runtime__.js';
var __name__ = '__main__';

if (!Object.entries) {
    Object.entries = function( obj ){
        var ownProps = Object.keys( obj ),
            i = ownProps.length,
            resArray = new Array(i);
        while (i--)
        resArray[i] = [ownProps[i], obj[ownProps[i]]];
        
        return resArray;
    };
}
//IE polyfill
if (typeof (HTMLCollection.prototype [Symbol.iterator]) === 'undefined') {
	HTMLCollection.prototype [Symbol.iterator] = Array.prototype [Symbol.iterator];
	HTMLFormControlsCollection.prototype [Symbol.iterator] = Array.prototype [Symbol.iterator];
}
export var DEFAULT_MESSAGES_ID = 'django_messages';
export var handleMessages = function (data, messages_id) {
	if (typeof messages_id == 'undefined' || (messages_id != null && messages_id.hasOwnProperty ("__kwargtrans__"))) {;
		var messages_id = DEFAULT_MESSAGES_ID;
	};
	var msgs = getattr (data, messages_id, []);
	if (len (msgs) > 0) {
		var msg_div = document.getElementById (messages_id);
		var msg_elem = msg_div.querySelector ('.alert');
		msg_div.innerHTML = '';
		for (var msg of msgs) {
			var msg_node = msg_elem.cloneNode ();
			msg_node.className = 'alert';
			msg_node.classList.add (msg.tags);
			msg_node.innerHTML = msg.text;
			msg_div.appendChild (msg_node);
		}
		msg_div.style.removeProperty ('display');
	}
};
export var ajax = function (param) {
	if (window.XMLHttpRequest) {
		var xhr = new XMLHttpRequest ();
	}
	else {
		var xhr = new ActiveXObject ('Microsoft.XMLHTTP') ();
	}
	xhr.open (param.type, param.url);
	if (param.contentType) {
		var content_type = param.contentType;
	}
	else {
		var content_type = 'application/x-www-form-urlencoded; charset=UTF-8';
	}
	if (param.dataType) {
		xhr.responseType = param.dataType;
	}
	xhr.setRequestHeader ('Content-Type', content_type);
	xhr.setRequestHeader ('X-Requested-With', 'XMLHttpRequest');
	if (param.headers) {
		for (var [header, value] of Object.entries (param.headers)) {
			xhr.setRequestHeader (header, value);
		}
	}
	var xhr_onload = function () {
		if (xhr.status === 200) {
			try {
				param.success (JSON.parse (xhr.responseText), xhr.statusText, xhr);
			}
			catch (__except0__) {
				param.success (xhr.responseText, xhr.statusText, xhr);
			}
		}
		else if (param.error) {
			param.error (xhr, xhr.statusText, xhr.responseText);
		}
		else {
			alert ('ajax response error: ' + xhr.responseText);
		}
	};
	xhr.onload = xhr_onload;
	xhr.onerror = (function __lambda__ (x, y, z) {
		return param.error (xhr, xhr.statusText, 'Unknown Error Occured. Server response not received.');
	});
	if (param.beforeSend) {
		param.beforeSend (xhr, param);
	}
	if (param.data) {
		xhr.send (param.data);
	}
	else {
		xhr.send ();
	}
};
export var serialize = function (obj) {
	var s = [];
	for (var [key, value] of Object.entries (obj)) {
		s.append ((encodeURIComponent (key) + '=') + encodeURIComponent (value));
	}
	return '&'.join (s).py_replace ('/%20/', '+');
};
export var formSerialize = function (form) {
	var s = [];
	if (typeof (form) == 'object' && form.nodeName.toLowerCase () == 'form') {
		for (var field of form.elements) {
			if (field.name && !(field.disabled) && !__in__ (field.type, ['file', 'reset', 'submit', 'button'])) {
				if (field.type == 'select-multiple') {
					for (var option of py_reversed (field.options)) {
						if (option.selected) {
							s [s.length] = (encodeURIComponent (field.name) + '=') + encodeURIComponent (field.options [j].value);
						}
					}
				}
				else if (!__in__ (field.type, ['checkbox', 'radio']) || field.checked) {
					s [s.length] = (encodeURIComponent (field.name) + '=') + encodeURIComponent (field.value);
				}
			}
		}
	}
	return '&'.join (s).py_replace ('/%20/', '+');
};
export var formJSON = function (form) {
	var s = {};
	if (typeof (form) == 'object' && form.nodeName.toLowerCase () == 'form') {
		for (var field of form.elements) {
			if (field.name && !(field.disabled) && !__in__ (field.type, ['file', 'reset', 'submit', 'button'])) {
				if (field.type == 'select-multiple') {
					s [field.name] = [];
					for (var option of py_reversed (field.options)) {
						if (option.selected) {
							s [field.name].append (option.value);
						}
					}
				}
				else if (!__in__ (field.type, ['checkbox', 'radio'])) {
					s [field.name] = field.value;
				}
				else if (field.checked) {
					if (!(s [field.name])) {
						s [field.name] = field.value;
					}
					else if (py_typeof (s [field.name]) !== list) {
						s [field.name] = [s [field.name]];
						s [field.name].append (field.value);
					}
					else {
						s [field.name].append (field.value);
					}
				}
			}
		}
	}
	return JSON.stringify (s);
};
export var csrfCompat = function (xhr, settings) {
	if (!(csrfSafeMethod (settings.py_type)) && sameOrigin (settings.url)) {
		xhr.setRequestHeader ('X-CSRFToken', getCookie ('csrftoken'));
	}
};
export var getCookie = function (cookie_name) {
	var cookie_value = null;
	if (document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split (';');
		for (var cookie of cookies) {
			var cookie = cookie.strip ();
			if (cookie.__getslice__ (0, len (cookie_name) + 1, 1) == cookie_name + '=') {
				var cookie_value = decodeURIComponent (cookie.__getslice__ (len (cookie_name) + 1, null, 1));
				break;
			}
		}
	}
	return cookie_value;
};
export var csrfSafeMethod = function (method) {
	return '/^(GET|HEAD|OPTIONS|TRACE)$/'.test (method);
};
export var sameOrigin = function (url) {
	var host = document.location.host;
	var protocol = document.location.protocol;
	var sr_origin = '//' + host;
	var origin = protocol + sr_origin;
	return (url == origin || url.slice (0, origin.length + 1) == origin + '/') || (url == sr_origin || url.slice (0, sr_origin.length + 1) == sr_origin + '/') || !('/^(\\/\\/|http:|https:).*/'.test (url));
};

//# sourceMappingURL=ajaxUtils.map