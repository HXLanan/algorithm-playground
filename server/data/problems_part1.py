# -*- coding: utf-8 -*-
"""题库数据层（第一部分）：数组与哈希 / 双指针 / 滑动窗口 / 二分查找。

纯数据，不含逻辑。每道题的字段说明见 ARCHITECTURE.md 第十一节。

字段：
  slug        唯一标识（与 LeetCode 一致）
  lcId        LeetCode 题号
  title       中文标题
  difficulty  难度（简单/中等/困难）
  tags        算法标签
  category    题库分类
  visualizer  关联的可视化页（可为 None）
  visHint     关联说明
  desc        题目描述
  examples    示例（含用于判题的输入输出）
  hints       提示
  solutions   参考解法（name/time/space/idea/code）
  funcName    判题时调用的函数名
  testCases   判题用测试用例 [{args:[...], expect:...}]
"""

PART1 = [
    {
        "slug": "two-sum", "lcId": 1, "title": "两数之和",
        "difficulty": "简单", "tags": ["数组", "哈希表"], "category": "数组与哈希",
        "visualizer": "sort.html", "visHint": "理解数组遍历与索引操作的基础",
        "desc": "给定一个整数数组 nums 和一个目标值 target，请找出数组中和为目标值的两个整数，并返回它们的下标。你可以假设每种输入只会对应一个答案，且不能重复使用同一个元素。",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0,1]",
             "explain": "nums[0] + nums[1] = 2 + 7 = 9"},
            {"input": "nums = [3,2,4], target = 6", "output": "[1,2]"},
        ],
        "hints": ["暴力双重循环是 O(n²)", "用哈希表把「查找补数」降到 O(1)"],
        "funcName": "two_sum",
        "testCases": [
            {"args": [[2, 7, 11, 15], 9], "expect": [0, 1]},
            {"args": [[3, 2, 4], 6], "expect": [1, 2]},
            {"args": [[3, 3], 6], "expect": [0, 1]},
        ],
        "solutions": [
            {"name": "哈希表（推荐）", "time": "O(n)", "space": "O(n)",
             "idea": "遍历数组，每遇到一个数 x，先查哈希表里有没有 target-x；有就返回，没有就把 x 和它的下标存进去。",
             "code": """def two_sum(nums, target):
    seen = {}                      # 值 -> 下标
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []"""},
            {"name": "暴力枚举", "time": "O(n²)", "space": "O(1)",
             "idea": "两层循环枚举所有数对，检查和是否等于 target。",
             "code": """def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []"""},
        ],
    },
    {
        "slug": "contains-duplicate", "lcId": 217, "title": "存在重复元素",
        "difficulty": "简单", "tags": ["数组", "哈希表", "排序"], "category": "数组与哈希",
        "visualizer": "sort.html", "visHint": "排序后相同元素会相邻，便于检测重复",
        "desc": "给你一个整数数组 nums。如果任一值在数组中出现至少两次，返回 true；如果数组中每个元素互不相同，返回 false。",
        "examples": [
            {"input": "nums = [1,2,3,1]", "output": "true"},
            {"input": "nums = [1,2,3,4]", "output": "false"},
        ],
        "hints": ["哈希集合记录见过的数", "排序后检查相邻元素"],
        "funcName": "contains_duplicate",
        "testCases": [
            {"args": [[1, 2, 3, 1]], "expect": True},
            {"args": [[1, 2, 3, 4]], "expect": False},
            {"args": [[]], "expect": False},
        ],
        "solutions": [
            {"name": "哈希集合", "time": "O(n)", "space": "O(n)",
             "idea": "边遍历边把元素放进集合，如果发现已经在集合里就说明重复了。",
             "code": """def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False"""},
            {"name": "排序后比较相邻", "time": "O(n log n)", "space": "O(1)",
             "idea": "排序后重复元素必然相邻，只需扫一遍比相邻两项。",
             "code": """def contains_duplicate(nums):
    a = sorted(nums)
    for i in range(1, len(a)):
        if a[i] == a[i - 1]:
            return True
    return False"""},
        ],
    },
    {
        "slug": "move-zeroes", "lcId": 283, "title": "移动零",
        "difficulty": "简单", "tags": ["数组", "双指针"], "category": "双指针",
        "visualizer": "sliding-window.html", "visHint": "双指针思想的入门应用",
        "desc": "给定一个数组 nums，编写一个函数将所有 0 移动到数组的末尾，同时保持非零元素的相对顺序。必须在不复制数组的情况下原地操作。",
        "examples": [
            {"input": "nums = [0,1,0,3,12]", "output": "[1,3,12,0,0]"},
            {"input": "nums = [0]", "output": "[0]"},
        ],
        "hints": ["用一个慢指针指向下一个非零元素该放的位置"],
        "funcName": "move_zeroes",
        "testCases": [
            {"args": [[0, 1, 0, 3, 12]], "expect": [1, 3, 12, 0, 0]},
            {"args": [[0]], "expect": [0]},
            {"args": [[1, 2, 3]], "expect": [1, 2, 3]},
        ],
        "solutions": [
            {"name": "快慢双指针", "time": "O(n)", "space": "O(1)",
             "idea": "慢指针 slow 指向下一个该放非零数的位置。快指针扫一遍，遇到非零就写到 slow 处并 slow+1。最后把 slow 之后全填 0。",
             "code": """def move_zeroes(nums):
    slow = 0
    for fast in range(len(nums)):
        if nums[fast] != 0:
            nums[slow] = nums[fast]
            slow += 1
    for i in range(slow, len(nums)):
        nums[i] = 0
    return nums"""},
        ],
    },
    {
        "slug": "valid-palindrome", "lcId": 125, "title": "验证回文串",
        "difficulty": "简单", "tags": ["字符串", "双指针"], "category": "双指针",
        "visualizer": "sliding-window.html", "visHint": "相向双指针的经典应用",
        "desc": "如果在将所有大写字符转换为小写字符、并移除所有非字母数字字符之后，短语正着读和反着读都一样，则认为是一个回文串。",
        "examples": [
            {"input": 's = "A man, a plan, a canal: Panama"', "output": "true"},
            {"input": 's = "race a car"', "output": "false"},
        ],
        "hints": ["左右两个指针向中间靠拢，遇到非字母数字就跳过"],
        "funcName": "is_palindrome",
        "testCases": [
            {"args": ["A man, a plan, a canal: Panama"], "expect": True},
            {"args": ["race a car"], "expect": False},
            {"args": [" "], "expect": True},
        ],
        "solutions": [
            {"name": "相向双指针", "time": "O(n)", "space": "O(1)",
             "idea": "left 从左、right 从右，各自跳过非字母数字字符，然后比较是否相等。",
             "code": """def is_palindrome(s):
    s = s.lower()
    left, right = 0, len(s) - 1
    while left < right:
        while left < right and not s[left].isalnum():
            left += 1
        while left < right and not s[right].isalnum():
            right -= 1
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True"""},
        ],
    },
    {
        "slug": "three-sum", "lcId": 15, "title": "三数之和",
        "difficulty": "中等", "tags": ["数组", "双指针", "排序"], "category": "双指针",
        "visualizer": "sort.html", "visHint": "排序后固定一个数，剩下两个用双指针夹逼",
        "desc": "给你一个整数数组 nums，判断是否存在三元组 [nums[i], nums[j], nums[k]] 满足 i != j、i != k 且 j != k，同时还满足 nums[i] + nums[j] + nums[k] == 0。返回所有和为 0 且不重复的三元组。",
        "examples": [
            {"input": "nums = [-1,0,1,2,-1,-4]", "output": "[[-1,-1,2],[-1,0,1]]"},
            {"input": "nums = [0,1,1]", "output": "[]"},
        ],
        "hints": ["先排序", "固定第一个数，后两个数用双指针向中间夹", "注意去重"],
        "funcName": "three_sum",
        "testCases": [
            {"args": [[-1, 0, 1, 2, -1, -4]], "expect": [[-1, -1, 2], [-1, 0, 1]]},
            {"args": [[0, 1, 1]], "expect": []},
            {"args": [[0, 0, 0]], "expect": [[0, 0, 0]]},
        ],
        "solutions": [
            {"name": "排序 + 双指针", "time": "O(n²)", "space": "O(1)",
             "idea": "排序后枚举第一个数 i，然后在 i 右侧用左右指针找两数之和为 -nums[i]。遇到重复值跳过以避免重复三元组。",
             "code": """def three_sum(nums):
    nums = sorted(nums)
    res = []
    n = len(nums)
    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:
            break
        left, right = i + 1, n - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s == 0:
                res.append([nums[i], nums[left], nums[right]])
                while left < right and nums[left] == nums[left + 1]:
                    left += 1
                while left < right and nums[right] == nums[right - 1]:
                    right -= 1
                left += 1
                right -= 1
            elif s < 0:
                left += 1
            else:
                right -= 1
    return res"""},
        ],
    },
    {
        "slug": "max-area", "lcId": 11, "title": "盛最多水的容器",
        "difficulty": "中等", "tags": ["数组", "双指针", "贪心"], "category": "双指针",
        "visualizer": "sliding-window.html", "visHint": "双指针收缩策略可视化",
        "desc": "给定一个长度为 n 的整数数组 height。有 n 条垂线，第 i 条线的两个端点是 (i, 0) 和 (i, height[i])。找出其中的两条线，使得它们与 x 轴共同构成的容器可以容纳最多的水。返回容器可以储存的最大水量。",
        "examples": [
            {"input": "height = [1,8,6,2,5,4,8,3,7]", "output": "49",
             "explain": "选择下标 1 和 8，水量 = min(8,7) × 7 = 49"},
        ],
        "hints": ["面积 = min(两边高度) × 底边宽度", "每次移动较矮的那一边"],
        "funcName": "max_area",
        "testCases": [
            {"args": [[1, 8, 6, 2, 5, 4, 8, 3, 7]], "expect": 49},
            {"args": [[1, 1]], "expect": 1},
            {"args": [[4, 3, 2, 1, 4]], "expect": 16},
        ],
        "solutions": [
            {"name": "相向双指针", "time": "O(n)", "space": "O(1)",
             "idea": "左右指针从两端向中间收缩。每次计算当前面积并更新最大值，然后移动高度较小的那一侧——因为移动较高侧只会让面积更小。",
             "code": """def max_area(height):
    left, right = 0, len(height) - 1
    best = 0
    while left < right:
        h = min(height[left], height[right])
        best = max(best, h * (right - left))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1
    return best"""},
        ],
    },
    {
        "slug": "length-of-longest-substring", "lcId": 3,
        "title": "无重复字符的最长子串",
        "difficulty": "中等", "tags": ["字符串", "滑动窗口", "哈希表"], "category": "滑动窗口",
        "visualizer": "sliding-window.html", "visHint": "这就是该可视化页演示的核心题目",
        "desc": "给定一个字符串 s，请你找出其中不含有重复字符的最长子串的长度。",
        "examples": [
            {"input": 's = "abcabcbb"', "output": "3", "explain": "最长子串是 \"abc\""},
            {"input": 's = "bbbbb"', "output": "1"},
            {"input": 's = "pwwkew"', "output": "3"},
        ],
        "hints": ["滑动窗口", "用哈希表记录字符最后出现的下标", "左指针可以直接跳到重复字符的下一位"],
        "funcName": "length_of_longest_substring",
        "testCases": [
            {"args": ["abcabcbb"], "expect": 3},
            {"args": ["bbbbb"], "expect": 1},
            {"args": ["pwwkew"], "expect": 3},
            {"args": [""], "expect": 0},
        ],
        "solutions": [
            {"name": "滑动窗口 + 哈希表", "time": "O(n)", "space": "O(min(n,Σ))",
             "idea": "右指针不断扩张；遇到重复字符时，左指针直接跳到该字符上次出现位置的下一位（不必一格一格挪）。",
             "code": """def length_of_longest_substring(s):
    last = {}
    left = 0
    best = 0
    for right, ch in enumerate(s):
        if ch in last and last[ch] >= left:
            left = last[ch] + 1
        last[ch] = right
        best = max(best, right - left + 1)
    return best"""},
        ],
    },
    {
        "slug": "min-subarray-len", "lcId": 209, "title": "长度最小的子数组",
        "difficulty": "中等", "tags": ["数组", "滑动窗口"], "category": "滑动窗口",
        "visualizer": "sliding-window.html", "visHint": "「求最短」型滑动窗口的范例",
        "desc": "给定一个含有 n 个正整数的数组和一个正整数 target。找出该数组中满足其总和大于等于 target 的长度最小的连续子数组，并返回其长度。如果不存在符合条件的子数组，返回 0。",
        "examples": [
            {"input": "target = 7, nums = [2,3,1,2,4,3]", "output": "2",
             "explain": "子数组 [4,3] 是该条件下的长度最小的子数组"},
        ],
        "hints": ["右指针扩张直到满足条件", "然后左指针收缩，记录最短"],
        "funcName": "min_sub_array_len",
        "testCases": [
            {"args": [7, [2, 3, 1, 2, 4, 3]], "expect": 2},
            {"args": [4, [1, 4, 4]], "expect": 1},
            {"args": [11, [1, 1, 1, 1, 1, 1]], "expect": 0},
        ],
        "solutions": [
            {"name": "不定长滑动窗口", "time": "O(n)", "space": "O(1)",
             "idea": "右指针扩张累加和；一旦和 ≥ target，就不断尝试收缩左边界并更新最短长度，直到不再满足条件。",
             "code": """def min_sub_array_len(target, nums):
    left = 0
    total = 0
    best = len(nums) + 1
    for right in range(len(nums)):
        total += nums[right]
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return best if best <= len(nums) else 0"""},
        ],
    },
    {
        "slug": "binary-search", "lcId": 704, "title": "二分查找",
        "difficulty": "简单", "tags": ["数组", "二分查找"], "category": "二分查找",
        "visualizer": "binary-search.html", "visHint": "本可视化页的对应题目",
        "desc": "给定一个 n 个元素有序的（升序）整型数组 nums 和一个目标值 target，写一个函数搜索 nums 中的 target，如果目标值存在返回下标，否则返回 -1。",
        "examples": [
            {"input": "nums = [-1,0,3,5,9,12], target = 9", "output": "4"},
            {"input": "nums = [-1,0,3,5,9,12], target = 2", "output": "-1"},
        ],
        "hints": ["左右边界不断收缩", "注意 while 用 <= 还是 <"],
        "funcName": "search",
        "testCases": [
            {"args": [[-1, 0, 3, 5, 9, 12], 9], "expect": 4},
            {"args": [[-1, 0, 3, 5, 9, 12], 2], "expect": -1},
            {"args": [[5], 5], "expect": 0},
        ],
        "solutions": [
            {"name": "标准二分", "time": "O(log n)", "space": "O(1)",
             "idea": "维护左闭右闭区间 [left, right]，每次取中点比较，根据大小收缩区间。",
             "code": """def search(nums, target):
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1"""},
        ],
    },
    {
        "slug": "search-range", "lcId": 34,
        "title": "在排序数组中查找元素的第一个和最后一个位置",
        "difficulty": "中等", "tags": ["数组", "二分查找"], "category": "二分查找",
        "visualizer": "binary-search.html", "visHint": "二分查找的两个变体（lower_bound / upper_bound）",
        "desc": "给你一个按照非递减顺序排列的整数数组 nums，和一个目标值 target。请你找出给定目标值在数组中的开始位置和结束位置。如果数组中不存在目标值，返回 [-1, -1]。",
        "examples": [
            {"input": "nums = [5,7,7,8,8,10], target = 8", "output": "[3,4]"},
            {"input": "nums = [5,7,7,8,8,10], target = 6", "output": "[-1,-1]"},
        ],
        "hints": ["分别找「第一个 ≥ target」和「第一个 > target」", "两个边界函数都基于二分"],
        "funcName": "search_range",
        "testCases": [
            {"args": [[5, 7, 7, 8, 8, 10], 8], "expect": [3, 4]},
            {"args": [[5, 7, 7, 8, 8, 10], 6], "expect": [-1, -1]},
            {"args": [[], 0], "expect": [-1, -1]},
        ],
        "solutions": [
            {"name": "两次二分（lower/upper bound）", "time": "O(log n)", "space": "O(1)",
             "idea": "写两个辅助函数：lower_bound 找第一个 ≥ target 的位置，upper_bound 找第一个 > target 的位置。答案就是 [lower, upper-1]。",
             "code": """def search_range(nums, target):
    def lower_bound(t):
        lo, hi = 0, len(nums)
        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < t:
                lo = mid + 1
            else:
                hi = mid
        return lo

    left = lower_bound(target)
    if left == len(nums) or nums[left] != target:
        return [-1, -1]
    right = lower_bound(target + 1) - 1
    return [left, right]"""},
        ],
    },
    {
        "slug": "sqrt-x", "lcId": 69, "title": "x 的平方根",
        "difficulty": "简单", "tags": ["数学", "二分查找"], "category": "二分查找",
        "visualizer": "binary-search.html", "visHint": "在答案空间上做二分（二分答案）",
        "desc": "给你一个非负整数 x，计算并返回 x 的算术平方根。由于返回类型是整数，结果只保留整数部分，小数部分将被舍去。",
        "examples": [
            {"input": "x = 4", "output": "2"},
            {"input": "x = 8", "output": "2", "explain": "8 的算术平方根是 2.82842...，舍去小数部分得 2"},
        ],
        "hints": ["在 [0, x] 范围内二分找最大的 m 使 m² ≤ x"],
        "funcName": "my_sqrt",
        "testCases": [
            {"args": [4], "expect": 2},
            {"args": [8], "expect": 2},
            {"args": [0], "expect": 0},
            {"args": [1], "expect": 1},
        ],
        "solutions": [
            {"name": "二分答案", "time": "O(log x)", "space": "O(1)",
             "idea": "答案一定在 [0, x] 中。二分这个区间，找满足 m*m <= x 的最大 m。",
             "code": """def my_sqrt(x):
    lo, hi = 0, x
    ans = 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if mid * mid <= x:
            ans = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return ans"""},
        ],
    },
]
