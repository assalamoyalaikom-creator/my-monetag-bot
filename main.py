import os
import time
import random
import zipfile
import telebot
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- ১. কনফিগারেশন ---
API_TOKEN = '8770622353:AAHzdBbNBFlmTbKcMcOgKlwZe8Ei4qHcrKM'
BLOG_LINK = 'https://12rahim.blogspot.com/'
bot = telebot.TeleBot(API_TOKEN)
is_running = False

# --- ২. প্রক্সি লিস্ট ---
RAW_PROXIES = [
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_01033247_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_85821338_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_93152772_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_45464860_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_46868658_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_13381813_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_40723687_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_99189892_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_29243813_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_99553129_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_73903543_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_11128436_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_24655735_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_01162268_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_TZ_st__city_sid_75829957_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_02438313_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_04279190_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_13581759_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_04761145_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_18414968_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_85127730_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_10571172_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_91328719_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_59502360_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_20260085_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_55351426_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_97188535_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_92426812_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_46523661_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UA_st__city_sid_71585609_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_26121347_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_75161758_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_72977077_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_80388334_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_48309378_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_12495909_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_75416342_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_01082247_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_38524990_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_48737835_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_56518514_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_71244814_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_31688929_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_13844850_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_UG_st__city_sid_34820156_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_88543929_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_28866073_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_15930537_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_80839637_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_84105240_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_32027410_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_08643200_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_67779962_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_04484789_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_96334419_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_90482209_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_37182669_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_90485737_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_56034478_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_GB_st__city_sid_12173474_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_69788428_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_57112826_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_98112349_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_10997455_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_86950249_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_33286257_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_87325804_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_27993441_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_27229800_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_29256532_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_87573271_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_20696774_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_23083812_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_05019625_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_US_st__city_sid_61789032_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_76069447_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_68198074_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_23671546_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_76107496_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_64410970_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_84340792_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_94748466_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_35485897_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_08501081_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_14019475_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_97328358_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_32808596_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_60939624_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_88468456_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MT_st__city_sid_93495970_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_09648899_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_46090403_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_85779139_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_63220122_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_82126642_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_81333865_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_73459200_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_15242567_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_15704014_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_87967097_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_18766902_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_17732278_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_60054106_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_23722852_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_ML_st__city_sid_19008903_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_26399814_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_36703888_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_47250271_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_20623978_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_49446814_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_87437570_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_12445662_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_98971681_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_80948392_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_48655502_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_81823860_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_45063197_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_86031157_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_90948445_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MD_st__city_sid_06560530_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_27638461_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_91475743_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_60326650_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_16528728_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_22368376_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_62933881_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_44416967_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_91250485_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_55912261_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_68203110_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_39561259_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_34763475_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_48661122_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_02168214_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_MA_st__city_sid_68950606_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_61194075_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_92421788_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_56192891_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_39628569_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_51065572_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_23990865_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_96488562_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_19141170_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_92057036_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_76596930_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_80797369_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_30975038_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_64526752_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_83549837_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_LY_st__city_sid_15579383_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_05019595_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_80921180_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_16792849_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_43590329_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_01099160_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_32303184_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_17296174_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_63206518_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_25768533_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_65789100_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_74848914_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_86176365_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_47816239_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_23370823_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_KE_st__city_sid_90418905_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_50975527_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_29089642_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_50515519_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_68061454_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_83930802_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_16192937_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_14720857_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_89444058_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_26629106_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_42689410_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_50121128_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_74479097_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_32268181_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_94517837_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_JP_st__city_sid_47873978_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_82476075_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_93926396_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_77468589_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_63613707_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_94649648_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_82254071_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_67952754_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_87673122_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_34332720_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_66685255_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_75283494_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_65355663_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_15138210_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_73639186_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IR_st__city_sid_65989259_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_62115651_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_49290860_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_44183304_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_72859433_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_41328657_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_12142904_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_78400811_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_22659452_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_22186879_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_53737642_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_51003360_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_72556804_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_05774157_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_45224674_time_5:2325276",
    "change4.owlproxy.com:7778:G67RxG84ts40_custom_zone_IT_st__city_sid_12535584_time_5:2325276"
]

# ডুপ্লিকেট বাদ দেওয়া
PROXIES = list(set(RAW_PROXIES))

# --- ৩. প্রক্সি চেক লজিক ---
def is_proxy_working(proxy_host, proxy_port, proxy_user, proxy_pass):
    proxy_url = f"http://{proxy_user}:{proxy_pass}@{proxy_host}:{proxy_port}"
    try:
        response = requests.get("http://www.google.com", proxies={"http": proxy_url, "https": proxy_url}, timeout=10)
        return response.status_code == 200
    except:
        return False

# --- ৪. প্রক্সি অথেনটিকেশন প্লাগইন ---
def create_proxy_auth_extension(proxy_host, proxy_port, proxy_user, proxy_pass):
    manifest_json = """
    {
        "version": "1.0.0", "manifest_version": 2, "name": "Chrome Proxy",
        "permissions": ["proxy", "tabs", "unlimitedStorage", "storage", "<all_urls>", "webRequest", "webRequestBlocking"],
        "background": {"scripts": ["background.js"]}
    }
    """
    background_js = """
    var config = { mode: "fixed_servers", rules: { singleProxy: { scheme: "http", host: "%s", port: parseInt(%s) } } };
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    function callbackFn(details) { return { authCredentials: { username: "%s", password: "%s" } }; }
    chrome.webRequest.onAuthRequired.addListener(callbackFn, {urls: ["<all_urls>"]}, ['blocking']);
    """ % (proxy_host, proxy_port, proxy_user, proxy_pass)
    
    plugin_path = f'proxy_plugin_{random.randint(1000, 9999)}.zip'
    with zipfile.ZipFile(plugin_path, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return plugin_path

# --- ৫. মূল অটোমেশন ---
def run_automation(chat_id):
    global is_running
    count = 1
    while is_running:
        driver = None
        plugin_path = None
        try:
            proxy_raw = random.choice(PROXIES)
            parts = proxy_raw.split(':')
            host, port, user, password = parts[0], parts[1], parts[2], parts[3]

            if not is_proxy_working(host, port, user, password):
                continue 

            options = Options()
            options.add_argument('--headless=new')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            options.add_extension(create_proxy_auth_extension(host, port, user, password))

            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            
            driver.get(BLOG_LINK)
            bot.send_message(chat_id, f"✅ সেশন {count}: প্রক্সি {host} সাকসেসফুল।")
            time.sleep(20)

        except Exception as e:
            print(f"Error: {e}")
        finally:
            if driver: driver.quit()
            count += 1
            time.sleep(60)

# --- ৬. টেলিগ্রাম কমান্ড ---
@bot.message_handler(commands=['work'])
def start(message):
    global is_running
    if not is_running:
        is_running = True
        bot.reply_to(message, "🚀 কাজ শুরু হয়েছে!")
        run_automation(message.chat.id)

@bot.message_handler(commands=['stop'])
def stop(message):
    global is_running
    is_running = False
    bot.reply_to(message, "🛑 বট বন্ধ হয়েছে।")

bot.polling(none_stop=True)
