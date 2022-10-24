import re

from datetime import datetime
from pydantic import BaseModel, Field, validator
from user_agents import parse

from models.basic_information import GenderType, MarriageType, PurposeType
from models.employment import EmployeeType, InsuranceType
from models.residence_information import HousingType, LivingTogetherType
from models.workplace import BusinessType, CompanySizeType


# 全角のみ許容する
FULL_WIDTH = "^([ぁ-ゖゝゞァ-ヷー一-龥丑-響々]+)$"
# カタカナのみ許容する
KATAKANA = "^([ァ-ワヲ-ヷー]+)$"
# 全半角文字入力時の許容文字で構成されているか
VALID_CHARS = "^([ぁ-ゖゝゞァ-ヷｱ-ﾝー一-龥丑-響々０-９ａ-ｚＡ-Ｚ　！”＃＄％＆’（）＊＋，−．／：；＜＝＞？＠［￥］＾＿｀｛｜｝〜。、・「」0-9a-zA-Z !#$%&'()*+,-.\/:;<=>?@\[\]^_`{|}~｡､･｢｣\"])+$"


class BaseApplication(BaseModel):
    user_agent: str
    last_name: str = Field(min_length=1, max_length=18)
    first_name: str = Field(min_length=1, max_length=18)
    kana_last_name: str = Field(min_length=1, max_length=28)
    kana_first_name: str = Field(min_length=1, max_length=28)
    birthday_year: str = Field(min_length=4, max_length=4)
    birthday_month: str = Field(min_length=2, max_length=2)
    birthday_day: str = Field(min_length=1, max_length=2)
    mobile_phone_number: str = Field(max_length=11)
    home_phone_number: str = Field(max_length=11)
    preferred_contact: str = Field("", min_length=1)
    yearly_salary: int = Field(ge=0, le=9999999)
    desired_amount: int = Field(ge=1, le=400)
    visit_url: str = Field(max_length=2000)
    gender: str = Field(min_length=1)
    purpose: str = Field(min_length=1)
    marriage: str = Field(min_length=1)
    postal_code: str = Field(min_length=7, max_length=7)
    address: str = Field(max_length=32)
    block_number: str = Field(min_length=1, max_length=32)
    street: str = Field(max_length=31)
    address_code: str = Field(max_length=10)
    jis_address_code: str = Field(max_length=5)
    employee_type: str = Field(min_length=1)
    insurance_type: str = Field(min_length=1)
    pay_day: int = Field(ge=1, le=31)
    hire_date_year: str = Field(min_length=4, max_length=4)
    other_work: str = Field(max_length=20)
    company_name: str = Field(min_length=1, max_length=20)
    kana_company_name: str = Field(min_length=1, max_length=30)
    business_type: str = Field(min_length=1)
    company_size: str = Field(min_length=1)
    company_phone_number: str = Field(min_length=10, max_length=11)
    housing_type: str = Field(min_length=1)
    rent: int = Field(ge=0, le=999999999)
    move_in_year: str = Field(min_length=4, max_length=4)
    living_alone: str = Field(min_length=1)
    dependent_family: int = Field(ge=0, le=20)
    email: str = Field(min_length=7, max_length=50)
    pin_number: str = Field(min_length=4, max_length=4)

    class Config:
        orm_mode = True

    @validator("user_agent")
    def user_agent_validation(v):
        user_agent = parse(v)
        if user_agent.device.family == "Other":
            raise ValueError("入力された値が『許容デバイス』ではありません")
        return str(user_agent.device.family)

    @validator("last_name")
    def last_name_validation(v):
        if not re.match(FULL_WIDTH, v):
            raise ValueError("漢字氏名(姓)は全角で入力してください。")
        return v

    @validator("first_name")
    def first_name_validation(cls, v, values):
        if "last_name" in values:
            if not re.match(FULL_WIDTH, v):
                raise ValueError("漢字氏名(名)は全角で入力してください。")
            else:
                if not len(v + values["last_name"]) <= 19:
                    raise ValueError("漢字氏名(姓)と漢字氏名(名)は合計で19文字以内で入力してください。")
        else:
            raise ValueError("漢字氏名(姓)に誤りがあります。")
        return v

    @validator("kana_last_name")
    def kana_last_name_validation(v):
        if not re.match(KATAKANA, v):
            raise ValueError("カナ氏名（姓）は全角カナで入力してください。")
        return v

    @validator("kana_first_name")
    def kana_first_name_validation(cls, v, values):
        if "kana_last_name" in values:
            if not re.match(KATAKANA, v):
                raise ValueError("カナ氏名（名）は全角カナで入力してください。")
            else:
                if not len(v + values["kana_last_name"]) <= 29:
                    raise ValueError("カナ氏名(姓)とカナ氏名(名)は合計で29文字以内で入力してください。")
        else:
            raise ValueError("カナ氏名(姓)に誤りがあります。")
        return v

    @validator("birthday_year")
    def birthday_year_validation(v):
        if not re.match("^([0-9]{4})$", v):
            raise ValueError("誕生年に誤りがあります。")
        return v.title()

    @validator("birthday_month")
    def birthday_month_validation(v):
        if not 1 <= int(v) <= 12:
            raise ValueError("誕生月に誤りがあります。")
        return v.title()

    @validator("birthday_day")
    def birthday_day_validation(cls, v, values):
        if "birthday_year" in values and "birthday_month" in values:
            date = datetime.now()
            birthday_year = int(values["birthday_year"])
            birthday_month = int(values["birthday_month"])
            birthday_day = int(v)

            this_year = int(datetime.now().strftime("%Y"))
            this_month = int(date.strftime("%m"))
            today = int(date.strftime("%d"))

            # 年齢計算

            age = this_year - birthday_year
            if this_month < birthday_month:
                age -= 1
            elif this_month == birthday_month:
                if today < birthday_day:
                    age -= 1

            if not 1 <= int(v) <= 31:
                raise ValueError("生年月日の入力に誤りがあります。")
            else:
                if not 20 <= age <= 69:
                    raise ValueError("20歳以上、69歳以下の方が対象です。")
        else:
            raise ValueError("生年月日に誤りがあります。")
        return v

    @validator("birthday_day")
    def birthday_check(cls, v, values):
        newDataStr = "%04d/%02d/%02d" % (
            int(values["birthday_year"]),
            int(values["birthday_month"]),
            int(v),
        )
        datetime.strptime(newDataStr, "%Y/%m/%d")
        return v.title()

    @validator("mobile_phone_number")
    def mobile_phone_number_validation(v):
        if v:
            if not re.match("^[0-9]*$", v):
                raise ValueError("半角数字で入力してください。")
            else:
                if not re.match("^0[7-9]0[0-9]{8}$", v):
                    raise ValueError("携帯電話番号に誤りがあります。")
        return v

    @validator("home_phone_number")
    def home_phone_number_validation(cls, v, values):
        if "mobile_phone_number" not in values:
            if v:
                if not re.match("^[0-9]*$", v):
                    raise ValueError("半角数字で入力してください。")
                else:
                    if v[0:3] == "050":
                        if not re.match("^050[0-9]{8}$", v):
                            raise ValueError("自宅電話番号が11桁ではありません。")
                    else:
                        if not re.match("^[0-9]{10}$", v):
                            raise ValueError("自宅電話番号が10桁ではありません。")
            else:
                raise ValueError("携帯電話番号に誤りがあります。")
        else:
            if not values["mobile_phone_number"] and not v:
                raise ValueError("いずれか入力してください。")
            else:
                if v:
                    if not re.match("^[0-9]*$", v):
                        raise ValueError("半角数字のみで構成されていません。")
                    else:
                        if v[0:3] == "050":
                            if not re.match("^050[0-9]{8}$", v):
                                raise ValueError("自宅電話番号が11桁ではありません。")
                        else:
                            if not re.match("^[0-9]{10}$", v):
                                raise ValueError("自宅電話番号が10桁ではありません。")
        return v

    @validator("yearly_salary")
    def yearly_salary_validation(v):
        if not 0 <= v <= 9999999:
            raise ValueError("年収に誤りがあります。")
        return v

    @validator("desired_amount")
    def desired_amount_validation(v):
        if not 1 <= v <= 400:
            raise ValueError("ご希望の契約額に誤りがあります。")
        return v

    @validator("gender")
    def gender_validation(v):
        if v not in GenderType._member_names_:
            raise ValueError("性別が不適切な値です。")
        return GenderType[v].value

    @validator("purpose")
    def purpose_validation(v):
        if v not in PurposeType._member_names_:
            raise ValueError("資金用途が不適切な値です。")
        return PurposeType[v].value

    @validator("marriage")
    def marriage_validation(v):
        if v not in MarriageType._member_names_:
            raise ValueError("結婚有無が不適切な値です。")
        return MarriageType[v].value

    @validator("postal_code")
    def postal_code_validation(v):
        if not re.match("^([0-9]{7})$", v):
            raise ValueError("郵便番号に誤りがあります。")
        return v

    @validator("address")
    def address_validation(v):
        if v:
            if not re.match(VALID_CHARS, v):
                raise ValueError("市区町村は利用できない文字が含まれています。")
        return v

    @validator("block_number")
    def block_number_validation(v):
        if not re.match(VALID_CHARS, v):
            raise ValueError("番地は利用できない文字が含まれています。")
        return v

    @validator("street")
    def street_validation(cls, v, values):
        if "block_number" in values:
            if v:
                if not re.match(VALID_CHARS, v):
                    raise ValueError("建物名は利用できない文字が含まれています。")
                elif not len(v + values["block_number"]) <= 32:
                    raise ValueError("番地と建物名は合計で３２文字以内で入力してください。")
        else:
            raise ValueError("番地は必須です。")
        return v

    @validator("address_code")
    def address_code_validation(v):
        if v:
            if not re.match("^([A-Za-z0-9]{10})$", v):
                raise ValueError("住所コードに誤りがあります。")
        return v

    @validator("jis_address_code")
    def jis_address_code_validation(v):
        if v:
            if not re.match("^([0-9]{5})$", v):
                raise ValueError("JIS住所コードに誤りがあります。")
        return v

    @validator("housing_type")
    def housing_type_validation(v):
        if v not in HousingType._member_names_:
            raise ValueError("お住まいの種類が不適切な値です。")
        return HousingType[v].value

    @validator("rent")
    def rent_validation(v):
        if not 0 <= v <= 999999999:
            raise ValueError("月々の家賃・住宅ローン（円）に誤りがあります。")
        return v

    @validator("move_in_year")
    def move_in_year_validation(cls, v, values):
        this_year = int(datetime.now().strftime("%Y"))

        if not re.match("^([0-9]{4})$", v):
            raise ValueError("入居年に誤りがあります。")
        else:
            if "birthday_year" in values:
                if int(values["birthday_year"]) > int(v):
                    raise ValueError("入居年が生年月日以前です。")
                elif int(v) > this_year:
                    raise ValueError("入居年が未来です。")
            else:
                raise ValueError("生年月日に誤りがあります。")
        return v

    @validator("living_alone")
    def living_alone_validation(v):
        if v not in LivingTogetherType._member_names_:
            raise ValueError("同居有無が不適切な値です。")
        return LivingTogetherType[v].value

    @validator("dependent_family")
    def dependent_family_validation(v):
        if not 0 <= v <= 20:
            raise ValueError("扶養家族数に誤りがあります。")
        return v

    @validator("employee_type")
    def employee_type_validation(v):
        if v not in EmployeeType._member_names_:
            raise ValueError("雇用形態が不適切な値です。")
        return EmployeeType[v].value

    @validator("insurance_type")
    def ceo_validation(cls, v, values):
        if v not in InsuranceType._member_names_:
            raise ValueError("保健職種が不適切な値です。")
        elif "employee_type" in values:
            if (
                EmployeeType(values["employee_type"]) is not EmployeeType.CEO
                and InsuranceType[v] is InsuranceType.CEO
            ):
                raise ValueError("雇用形態で社長・代表者が選択されていません。")
            if (
                EmployeeType(values["employee_type"]) is EmployeeType.CEO
                and InsuranceType[v] is not InsuranceType.CEO
            ):
                raise ValueError("雇用形態で社長・代表者を選択している場合は０を選択してください。")
        else:
            raise ValueError("雇用形態に誤りがあります。")
        return InsuranceType[v].value

    @validator("pay_day")
    def pay_day_validation(v):
        if not 1 <= v <= 31:
            raise ValueError("給料日に誤りがあります。")
        return v

    @validator("hire_date_year")
    def hire_date_year_validation(cls, v, values):
        this_year = int(datetime.now().strftime("%Y"))

        if not re.match("^([0-9]{4})$", v):
            raise ValueError("入社年に誤りがあります。")
        else:
            if "birthday_year" in values:
                if int(values["birthday_year"]) > int(v) or int(v) > this_year:
                    raise ValueError("入社年に誤りがあります。")
            else:
                raise ValueError("生年月日に誤りあります。")
        return v

    @validator("other_work")
    def other_work_validation(v):
        if v:
            if not re.match(VALID_CHARS, v):
                raise ValueError("その他のお仕事は利用できない文字が含まれています。")
        return v

    @validator("company_name")
    def company_name_validation(v):
        if not re.match(VALID_CHARS, v):
            raise ValueError("勤務先名は利用できない文字が含まれています。")
        return v

    @validator("kana_company_name")
    def kana_company_name_validation(v):
        if not re.match(KATAKANA, v):
            raise ValueError("カナ勤務先名は全角カナで入力してください。")
        return v

    @validator("business_type")
    def business_type_validation(v):
        if v not in BusinessType._member_names_:
            raise ValueError("業種が不適切な値です。")
        return BusinessType[v].value

    @validator("company_size")
    def company_size_validation(v):
        if v not in CompanySizeType._member_names_:
            raise ValueError("会社規模が不適切な値です。")
        return CompanySizeType[v].value

    @validator("company_phone_number")
    def company_phone_number_validation(v):
        if not re.match("^[0-9]*$", v):
            raise ValueError("勤務先電話番号は半角数字で入力してください。")
        else:
            if re.match("^(0[1-9]0)$", v[0:3]):
                if not re.match("^(0[1-9]0[0-9]{8})$", v):
                    raise ValueError("勤務先電話番号が11桁ではありません。")
            else:
                if not re.match("^([0-9]{10})$", v):
                    raise ValueError("勤務先電話番号が10桁ではありません。")
        return v.title()

    @validator("email")
    def email_validation(v):
        # メールアドレスのRegex スマホ版アップフォームから引用
        pattern = "^([A-Za-z0-9\-#%*_+\/?{}|`$&]+(.[A-Za-z0-9\-#%*_+\/?{}|`$&]+)*)@[A-Za-z0-9]+(\.[A-Za-z0-9]+)$"
        if not re.match(pattern, v):
            raise ValueError("メールアドレスに誤りがあります。")
        return v.title()

    @validator("pin_number")
    def pin_number_validation(v):
        if not re.match("^([0-9]{4})+$", v):
            raise ValueError("パスワードは半角数字4桁で入力してください。")
        return v.title()

    def gender_marriage_combination(self):
        male_and_unmarried = 1
        female_and_unmarried = 2
        male_and_married = 3
        female_and_married = 4

        if self.gender == GenderType["MALE"].value:
            if self.marriage == MarriageType["MARRIED"].value:
                gender_marriage_combo = male_and_married
            else:
                gender_marriage_combo = male_and_unmarried
        else:
            if self.marriage == MarriageType["MARRIED"].value:
                gender_marriage_combo = female_and_married
            else:
                gender_marriage_combo = female_and_unmarried
        return gender_marriage_combo

    def parse_mobile_phone_number(self):
        parsed = {}
        parsed["initial_three"] = self.mobile_phone_number[0:3]
        parsed["local_area_code"] = self.mobile_phone_number[3:7]
        parsed["subscriber_number"] = self.mobile_phone_number[7:11]
        return parsed

    def parse_home_phone_number(self):
        parsed = {}
        parsed["area_code"] = self.home_phone_number[0:3]

        if parsed["area_code"] == "050":
            parsed["local_area_code"] = self.home_phone_number[3:7]
            parsed["subscriber_number"] = self.home_phone_number[7:11]
        else:
            parsed["local_area_code"] = self.home_phone_number[3:6]
            parsed["subscriber_number"] = self.home_phone_number[6:10]

        return parsed

    def parse_company_phone_number(self):
        parsed = {}
        parsed["area_code"] = self.company_phone_number[0:3]

        if re.match("^(0[1-9]0)$", parsed["area_code"]):
            parsed["local_area_code"] = self.company_phone_number[3:7]
            parsed["subscriber_number"] = self.company_phone_number[7:11]
        else:
            parsed["local_area_code"] = self.company_phone_number[3:6]
            parsed["subscriber_number"] = self.company_phone_number[6:10]

        return parsed

    def parse_preferred_contact(self):
        HOME_PHONE = 1
        MOBILE_PHONE = 2

        if self.mobile_phone_number:
            preferred_contact = MOBILE_PHONE
        else:
            preferred_contact = HOME_PHONE
        return preferred_contact
