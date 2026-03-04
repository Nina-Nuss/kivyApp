[app]

title = KugelSpiel
package.name = eigenesPaket
package.domain = gsog.eigeneDomain

source.dir = KugelSpiel
source.include_exts = py,png,jpg,kv,atlas,json,db,txt

version = 0.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,materialyoucolor,exceptiongroup,asyncgui,asynckivy,pillow,plyer
source.include_patterns = db/*.py,db/*.db,db/*.json,klassen/*.py,assets/*

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a

android.accept_sdk_license = True

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = main
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

icon.filename = nina/assets/logo.jpg

[buildozer]
log_level = 2
