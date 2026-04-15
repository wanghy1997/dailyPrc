import itchat


def export_group_members(group_name, output_file):
    # 登录微信
    itchat.auto_login(hotReload=True)

    # 获取群聊对象
    chatrooms = itchat.get_chatrooms(update=True)
    target_group = None
    for chatroom in chatrooms:
        if chatroom['NickName'] == group_name:
            target_group = chatroom
            break

    # 如果找到了目标群聊
    if target_group:
        members = itchat.update_chatroom(target_group['UserName'], detailedMember=True)['MemberList']

        with open(output_file, 'w', encoding='utf-8') as file:
            for member in members:
                nickname = member['NickName']
                remark_name = member['DisplayName'] or member['NickName']
                file.write(f"{nickname}, {remark_name}\n")

        print(f"群成员及其备注已导出到文件: {output_file}")
    else:
        print(f"未找到名称为 {group_name} 的群聊")


if __name__ == "__main__":
    group_name = input("请输入要导出的群聊名称：")
    output_file = input("请输入导出文件的路径和名称：")
    export_group_members(group_name, output_file)
