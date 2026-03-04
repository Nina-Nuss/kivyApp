[app]
title = KugelSpiel
package.name = kugelspiel
package.domain = gsog.schule

source.dir = KugelSpiel
source.include_exts = py,png,jpg,kv,atlas,json,db,txt
source.include_patterns = db/*.py,db/*.db,db/*.json,klassen/*.py,assets/*

version = 0.1
requirements = python3,kivy==2.3.0,kivymd==1.2.0,materialyoucolor,exceptiongroup,asyncgui,asynckivy,pillow,plyer

orientation = portrait
android.api = 33
android.minapi = 26
android.archs = arm64-v8a
android.accept_sdk_license = True

icon.filename = %(source.dir)s/assets/logo.jpg

[buildozer]
log_level = 2
