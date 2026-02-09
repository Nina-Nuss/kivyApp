[app]

title = KugelSpiel
package.name = eigenesPaket
package.domain = gsog.eigeneDomain

source.dir = jonas
source.include_exts = py,png,jpg,kv,atlas,json,db,txt

version = 0.1
requirements = python3,kivy,https://github.com/kivymd/KivyMD/archive/master.zip,materialyoucolor,exceptiongroup,asyncgui,asynckivy,pillow

orientation = portrait
fullscreen = 0
android.archs = arm64-v8a

android.accept_sdk_license = True

# iOS specific
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = main
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.7.0

[buildozer]
log_level = 2
