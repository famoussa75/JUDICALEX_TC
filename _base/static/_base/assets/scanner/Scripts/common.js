var dynamsoft = dynamsoft || {};

(function(){
	var _deviceType='pc',
		_strBrowserVersion = '',
		_mainVer = 0,
		_bUseUserAgent = false;

	if('userAgentData' in navigator) {

		var aryBrands=[],
			uaData = navigator['userAgentData'],
			_platform = uaData.platform.toLowerCase(),
			_i, _count;

		if('brands' in uaData && Array.isArray(uaData['brands']) && uaData['brands'].length>0) {
			aryBrands = uaData.brands;
		} else  if('uaList' in uaData && Array.isArray(uaData['uaList']) && uaData['uaList'].length>0) {
			aryBrands = uaData.uaList;
		}

		_count = aryBrands.length;
		
		if(_count == 0) {
			_bUseUserAgent = true;
		} else {
			var _bWin=false,_bEdge=false,_bChrome=false,_bOpera=false;

			for(_i=0;_i<_count;_i++){
				var brand = aryBrands[_i].brand.toLowerCase();
				if(brand.indexOf("chrome")>=0) {
					_bChrome=true;
					_strBrowserVersion = aryBrands[_i].version;
					break;
				} else if(brand.indexOf("edge")>=0) {
					_bEdge=true;
					_strBrowserVersion = aryBrands[_i].version;
					break;
				} else if(brand.indexOf("opera")>=0) {
					_bOpera=true;
					_strBrowserVersion = aryBrands[_i].version;
					break;
				}
			}

			if(!_bChrome && !_bEdge && !_bOpera) {
				_bChrome=true;
				_strBrowserVersion='100';
			}

			//_bMac = (_platform.indexOf('mac')>=0);
			_bChromeOS = (_platform.indexOf('chrome os')>=0);
			_bWin = (_platform == 'windows');
			//_bLinux = (_platform == 'linux');
			if (uaData.mobile) {
				_deviceType = 'phone'; 
			}

			if(_strBrowserVersion.indexOf('.') > -1)
				_mainVer = _strBrowserVersion.slice(0, _strBrowserVersion.indexOf('.')) * 1.0;

			dynamsoft.onlineNavInfo = {
			    bWin: _bWin,
			    bChromeOS: _bChromeOS,
				
				bIE: false,
				bEdge: _bEdge,
				bFirefox: false,
				bChrome: _bChrome,
				bSafari: false,
				
				strVersion: _strBrowserVersion,
				mainVer: _mainVer,
				deviceType: _deviceType
				
			};
		}

	} else {
		_bUseUserAgent = true;
	}

	if(_bUseUserAgent) {
		var ua = navigator.userAgent.toLowerCase(),
			_platform = navigator.platform.toLowerCase(),

			_bWin = (_platform == 'win32') || (_platform == 'win64') || (_platform == 'windows'),
			
			_nMSIE = ua.indexOf('msie'),
			_nTrident = ua.indexOf('trident'),
			_nRV = ua.indexOf('rv:'),
			_nEdge = ua.indexOf('edge'),

			_tmp = ua.match(/version\/([\d.]+).*safari/),
			_bSafari = _tmp ? !0 : !1,
			_nSafari = _tmp ? _tmp[1] : 0,

			_nFirefox = ua.indexOf('firefox'),
			_bFirefox = (_nFirefox != -1),
			
			_bEdge = _bWin && !_bFirefox && (_nEdge != -1),
			
			_indexOfChrome = ua.indexOf('chrome'),
			_bChrome =  !_bEdge && (_indexOfChrome != -1),

			_bIE = _bWin && !_bFirefox && !_bEdge && !_bChrome && (_nMSIE != -1 || _nTrident != -1 || _nRV != -1);
		

		var bPadOrMacDesktop = (/macintosh/i).test(ua), // maybe iPad or MAC Desktop
			bIsIpad = (/ipad/i).test(ua) || ((bPadOrMacDesktop||(_platform=='macintel')) && navigator.maxTouchPoints && navigator.maxTouchPoints > 1),
			bIsIphoneOs = ua.match(/iphone os/i) == "iphone os",
			bIsMidp = ua.match(/midp/i) == "midp",
			bIsUc7 = ua.match(/rv:1.2.3.4/i) == "rv:1.2.3.4",
			bIsUc = ua.match(/ucweb/i) == "ucweb",
			bIsAndroid = ua.match(/android/i) == "android",
			bIsCE = ua.match(/windows ce/i) == "windows ce",
			bIsWM = ua.match(/windows mobile/i) == "windows mobile";

		if(ua.indexOf("googlebot") >= 0) {
			// pc
		} else if (bIsIpad || bIsIphoneOs || bIsMidp || bIsUc7 || bIsUc || bIsAndroid || bIsCE || bIsWM) {
			_deviceType = 'phone'; 
		}


		if(_bEdge) {
			_tmp = ua.slice(_nEdge + 5);
			_tmp = _tmp.slice(0, _tmp.indexOf(' '));
			_strBrowserVersion = _tmp;
			
		} else if (_bChrome) {
			_tmp = ua.slice(_indexOfChrome + 7);
			_tmp = _tmp.slice(0, _tmp.indexOf(' '));
			_strBrowserVersion = _tmp;

		} else if (_bFirefox) {	// FF
			_tmp = ua.slice(_nFirefox + 8);
			_tmp = _tmp.slice(0, _tmp.indexOf(' '));
			_strBrowserVersion = _tmp;

		} else if (_bIE) {
			if (_nMSIE != -1) {
				// 'msie'
				_tmp = ua.slice(_nMSIE + 4);
				_tmp = _tmp.slice(0, _tmp.indexOf(';'));
				_strBrowserVersion = _tmp;
			} else if (_nRV != -1) {
				// 'rv:'
				_tmp = ua.slice(_nRV + 3);
				_tmp = _tmp.slice(0, _tmp.indexOf(';'));
				_tmp = _tmp.slice(0, _tmp.indexOf(')'));
				_strBrowserVersion = _tmp;
			} else if (_nTrident != -1) {
				// 'trident'
				_tmp = ua.slice(_nTrident + 7);
				_tmp = _tmp.slice(0, _tmp.indexOf(';'));
				_strBrowserVersion = _tmp;
			}


		} else if (_bSafari) {
			if (_tmp) {
				_strBrowserVersion = _tmp[1];
			}
		}

		if(_strBrowserVersion.indexOf('.') > -1)
			_mainVer = _strBrowserVersion.slice(0, _strBrowserVersion.indexOf('.')) * 1.0;
		
		dynamsoft.onlineNavInfo = {
			bWin: _bWin,
			
			bIE: _bIE,
			bEdge: _bEdge,
			bFirefox: _bFirefox,
			bChrome: _bChrome,
			bSafari: _bSafari,
			
			strVersion: _strBrowserVersion,
			mainVer: _mainVer,
			deviceType: _deviceType
			
		};
	}
})();
