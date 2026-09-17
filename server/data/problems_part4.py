# -*- coding: utf-8 -*-
"""题库数据层（第四部分）：哈希/前缀和/滑动窗口/二分查找 补强。

包含困难题，提高题库上限。
"""

PART4 = [
    {
        "slug": "group-anagrams", "lcId": 49, "title": "字母异位词分组",
        "difficulty": "中等", "tags": ["数组", "哈希表", "字符串", "排序"], "category": "数组与哈希",
        "visualizer": "sort.html", "visHint": "排序后的字符串作为哈希键",
        "desc": "给你一个字符串数组，请你将字母异位词组合在一起。可以按任意顺序返回结果列表。字母异位词是由重新排列源单词的所有字母得到的一个新单词。",
        "examples": [
            {"input": 'strs = ["eat","tea","tan","ate","nat","bat"]',
             "output": '[["bat"],["nat","tan"],["ate","eat","tea"]]'},
            {"input": 'strs = [""]', "output": '[[""]]'},
        ],
        "hints": ["异位词排序后是同一个字符串", "用排序结果作为哈希表的键"],
        "funcName": "group_anagrams",
        "testCases": [
            {"args": [["eat","tea","tan","ate","nat","bat"]],
             "expect": [["bat"],["nat","tan"],["ate","eat","tea"]]},
            {"args": [[""]], "expect": [[""]]},
            {"args": [["a"]], "expect": [["a"]]},
        ],
        "solutions": [
            {"name": "排序后作键", "time": "O(n·k log k)", "space": "O(n·k)",
             "idea": "把每个字符串的字符排序，排序结果相同的必然互为异位词。用这个结果当字典的键，把原字符串归到同一组。",
             "code": """def group_anagrams(strs):
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        groups[''.join(sorted(s))].append(s)
    return list(groups.values())"""},
            {"name": "字符计数作键", "time": "O(n·k)", "space": "O(n·k)",
             "idea": "用 26 个字母的计数元组当键，避免排序的 log k 开销。",
             "code": """def group_anagrams(strs):
    from collections import defaultdict
    groups = defaultdict(list)
    for s in strs:
        cnt = [0] * 26
        for ch in s:
            cnt[ord(ch) - ord('a')] += 1
        groups[tuple(cnt)].append(s)
    return list(groups.values())"""},
        ],
    },
    {
        "slug": "product-except-self", "lcId": 238, "title": "除自身以外数组的乘积",
        "difficulty": "中等", "tags": ["数组", "前缀和"], "category": "数组与哈希",
        "visualizer": None, "visHint": None,
        "desc": "给你一个整数数组 nums，返回数组 answer，其中 answer[i] 等于 nums 中除 nums[i] 之外其余各元素的乘积。题目数据保证数组 nums 之中任意元素的全部前缀元素和后缀的乘积都在 32 位整数范围内。请不要使用除法，且在 O(n) 时间复杂度内完成此题。",
        "examples": [
            {"input": "nums = [1,2,3,4]", "output": "[24,12,8,6]"},
            {"input": "nums = [-1,1,0,-3,3]", "output": "[0,0,9,0,0]"},
        ],
        "hints": ["不能用除法（因为有 0）", "answer[i] = 左侧所有数乘积 × 右侧所有数乘积"],
        "funcName": "product_except_self",
        "testCases": [
            {"args": [[1, 2, 3, 4]], "expect": [24, 12, 8, 6]},
            {"args": [[-1, 1, 0, -3, 3]], "expect": [0, 0, 9, 0, 0]},
        ],
        "solutions": [
            {"name": "左右前缀积", "time": "O(n)", "space": "O(1)",
             "idea": "先把「左侧所有数的乘积」填进答案数组；再从右往左遍历，用一个变量累积「右侧所有数的乘积」，与答案数组相乘。",
             "code": """def product_except_self(nums):
    n = len(nums)
    ans = [1] * n
    left = 1
    for i in range(n):
        ans[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        ans[i] *= right
        right *= nums[i]
    return ans"""},
        ],
    },
    {
        "slug": "longest-consecutive", "lcId": 128, "title": "最长连续序列",
        "difficulty": "中等", "tags": ["数组", "哈希表", "并查集"], "category": "数组与哈希",
        "visualizer": None, "visHint": None,
        "desc": "给定一个未排序的整数数组 nums，找出数字连续的最长序列（不要求序列元素在原数组中连续）的长度。请你设计并实现时间复杂度为 O(n) 的算法解决此问题。",
        "examples": [
            {"input": "nums = [100,4,200,1,3,2]", "output": "4", "explain": "最长连续序列是 [1,2,3,4]"},
            {"input": "nums = [0,3,7,2,5,8,4,6,0,1]", "output": "9"},
        ],
        "hints": ["用哈希集合实现 O(1) 查找", "只从「序列起点」（x-1 不在集合里）开始数"],
        "funcName": "longest_consecutive",
        "testCases": [
            {"args": [[100, 4, 200, 1, 3, 2]], "expect": 4},
            {"args": [[0, 3, 7, 2, 5, 8, 4, 6, 0, 1]], "expect": 9},
            {"args": [[]], "expect": 0},
        ],
        "solutions": [
            {"name": "哈希集合 + 只数起点", "time": "O(n)", "space": "O(n)",
             "idea": "把所有数放进集合。只对那些「x-1 不在集合里」的数（即序列起点）向后数，这样每个数最多被访问两次，整体 O(n)。",
             "code": """def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 in s:
            continue          # 不是起点，跳过
        cur = x
        length = 1
        while cur + 1 in s:
            cur += 1
            length += 1
        best = max(best, length)
    return best"""},
        ],
    },
    {
        "slug": "subarray-sum-k", "lcId": 560, "title": "和为 K 的子数组",
        "difficulty": "中等", "tags": ["数组", "哈希表", "前缀和"], "category": "数组与哈希",
        "visualizer": None, "visHint": None,
        "desc": "给你一个整数数组 nums 和一个整数 k，请你统计并返回该数组中和为 k 的子数组的个数。子数组是数组中元素的连续非空序列。",
        "examples": [
            {"input": "nums = [1,1,1], k = 2", "output": "2"},
            {"input": "nums = [1,2,3], k = 3", "output": "2"},
        ],
        "hints": ["不要求连续？错，是连续子数组", "用前缀和：sum[i..j] = pre[j] - pre[i-1]"],
        "funcName": "subarray_sum",
        "testCases": [
            {"args": [[1, 1, 1], 2], "expect": 2},
            {"args": [[1, 2, 3], 3], "expect": 2},
            {"args": [[1, -1, 0], 0], "expect": 3},
        ],
        "solutions": [
            {"name": "前缀和 + 哈希表", "time": "O(n)", "space": "O(n)",
             "idea": "维护前缀和 pre，并用哈希表记录「每个前缀和出现的次数」。当 pre - k 出现过 n 次时，说明有 n 个子数组的和为 k（注意处理数组含负数的情况）。",
             "code": """def subarray_sum(nums, k):
    count = {0: 1}
    pre = 0
    ans = 0
    for x in nums:
        pre += x
        if pre - k in count:
            ans += count[pre - k]
        count[pre] = count.get(pre, 0) + 1
    return ans"""},
        ],
    },
    {
        "slug": "min-window-substring", "lcId": 76, "title": "最小覆盖子串",
        "difficulty": "困难", "tags": ["字符串", "滑动窗口", "哈希表"], "category": "滑动窗口",
        "visualizer": "sliding-window.html", "visHint": "不定长滑动窗口的最难变体",
        "desc": "给你一个字符串 s、一个字符串 t。返回 s 中涵盖 t 所有字符的最小子串。如果 s 中不存在涵盖 t 所有字符的子串，则返回空字符串 \"\"。对于 t 中重复字符，我们寻找的子字符串中该字符数量必须不少于 t 中该字符数量。",
        "examples": [
            {"input": 's = "ADOBECODEBANC", t = "ABC"', "output": '"BANC"'},
            {"input": 's = "a", t = "a"', "output": '"a"'},
            {"input": 's = "a", t = "aa"', "output": '""'},
        ],
        "hints": ["用 need 记录 t 的字符需求", "右指针扩张到满足需求，再收缩左指针找最小"],
        "funcName": "min_window",
        "testCases": [
            {"args": ["ADOBECODEBANC", "ABC"], "expect": "BANC"},
            {"args": ["a", "a"], "expect": "a"},
            {"args": ["a", "aa"], "expect": ""},
        ],
        "solutions": [
            {"name": "滑动窗口 + 需求计数", "time": "O(n)", "space": "O(Σ)",
             "idea": "用 need 字典记录 t 中每个字符的需求量，window 记录当前窗口的计数。右指针扩张，当「已满足的字符种类数」等于 need 大小时，尝试收缩左指针并记录最小窗口。",
             "code": """def min_window(s, t):
    from collections import Counter
    if not t or not s:
        return ""
    need = Counter(t)
    window = {}
    have, required = 0, len(need)
    left = 0
    best_len = float('inf')
    best = ""
    for right, ch in enumerate(s):
        window[ch] = window.get(ch, 0) + 1
        if ch in need and window[ch] == need[ch]:
            have += 1
        while have == required:
            if right - left + 1 < best_len:
                best_len = right - left + 1
                best = s[left:right + 1]
            lc = s[left]
            window[lc] -= 1
            if lc in need and window[lc] < need[lc]:
                have -= 1
            left += 1
    return best"""},
        ],
    },
    {
        "slug": "find-anagrams", "lcId": 438, "title": "找到字符串中所有字母异位词",
        "difficulty": "中等", "tags": ["字符串", "滑动窗口", "哈希表"], "category": "滑动窗口",
        "visualizer": "sliding-window.html", "visHint": "定长滑动窗口的典型应用",
        "desc": "给定两个字符串 s 和 p，找到 s 中所有 p 的异位词的子串，返回这些子串的起始索引。不考虑答案输出的顺序。异位词指由相同字母重排列形成的字符串（包括相同的字符串）。",
        "examples": [
            {"input": 's = "cbaebabacd", p = "abc"', "output": "[0,6]"},
            {"input": 's = "abab", p = "ab"', "output": "[0,1,2]"},
        ],
        "hints": ["窗口大小固定为 len(p)", "维护窗口内字符计数与 p 的差异"],
        "funcName": "find_anagrams",
        "testCases": [
            {"args": ["cbaebabacd", "abc"], "expect": [0, 6]},
            {"args": ["abab", "ab"], "expect": [0, 1, 2]},
            {"args": ["a", "b"], "expect": []},
        ],
        "solutions": [
            {"name": "定长滑动窗口 + 计数比较", "time": "O(n)", "space": "O(Σ)",
             "idea": "窗口大小固定为 len(p)。滑动时只更新进出窗口的两个字符，每步比较窗口计数与 p 的计数是否相同。",
             "code": """def find_anagrams(s, p):
    from collections import Counter
    n, m = len(s), len(p)
    if m > n:
        return []
    need = Counter(p)
    window = Counter(s[:m])
    res = []
    if window == need:
        res.append(0)
    for i in range(m, n):
        window[s[i]] += 1
        out = s[i - m]
        window[out] -= 1
        if window[out] == 0:
            del window[out]
        if window == need:
            res.append(i - m + 1)
    return res"""},
        ],
    },
    {
        "slug": "max-sliding-window", "lcId": 239, "title": "滑动窗口最大值",
        "difficulty": "困难", "tags": ["数组", "滑动窗口", "单调队列", "堆"], "category": "滑动窗口",
        "visualizer": "sliding-window.html", "visHint": "滑动窗口 + 单调队列（进阶）",
        "desc": "给你一个整数数组 nums，有一个大小为 k 的滑动窗口从数组的最左侧移动到数组的最右侧。你只可以看到在滑动窗口内的 k 个数字。滑动窗口每次只向右移动一位。返回滑动窗口中的最大值。",
        "examples": [
            {"input": "nums = [1,3,-1,-3,5,3,6,7], k = 3",
             "output": "[3,3,5,5,6,7]"},
        ],
        "hints": ["暴力 O(n·k) 会超时", "用单调递减队列，队首永远是窗口最大值"],
        "funcName": "max_sliding_window",
        "testCases": [
            {"args": [[1, 3, -1, -3, 5, 3, 6, 7], 3], "expect": [3, 3, 5, 5, 6, 7]},
            {"args": [[1], 1], "expect": [1]},
            {"args": [[7, 2, 4], 2], "expect": [7, 4]},
        ],
        "solutions": [
            {"name": "单调队列（推荐）", "time": "O(n)", "space": "O(k)",
             "idea": "维护一个下标队列，队列里的值单调递减。新元素入队前，把队尾所有比它小的弹出（它们不可能是最大值了）；同时把滑出窗口的下标从队首移除。队首就是当前窗口最大值。",
             "code": """from collections import deque

def max_sliding_window(nums, k):
    dq = deque()          # 存下标，对应值单调递减
    res = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            res.append(nums[dq[0]])
    return res"""},
            {"name": "大顶堆", "time": "O(n log n)", "space": "O(n)",
             "idea": "把 (-值, 下标) 压入堆。每次取出堆顶，若下标已滑出窗口就丢弃，直到找到窗口内的最大值。",
             "code": """import heapq

def max_sliding_window(nums, k):
    heap = []
    res = []
    for i, x in enumerate(nums):
        heapq.heappush(heap, (-x, i))
        if i >= k - 1:
            while heap[0][1] <= i - k:
                heapq.heappop(heap)
            res.append(-heap[0][0])
    return res"""},
        ],
    },
    {
        "slug": "median-two-sorted", "lcId": 4, "title": "寻找两个正序数组的中位数",
        "difficulty": "困难", "tags": ["数组", "二分查找", "分治"], "category": "二分查找",
        "visualizer": "binary-search.html", "visHint": "在「分割线」上二分，二分查找的最高级用法",
        "desc": "给定两个大小分别为 m 和 n 的正序（从小到大）数组 nums1 和 nums2。请你找出并返回这两个正序数组的中位数。算法的时间复杂度应该为 O(log (m+n))。",
        "examples": [
            {"input": "nums1 = [1,3], nums2 = [2]", "output": "2.0"},
            {"input": "nums1 = [1,2], nums2 = [3,4]", "output": "2.5"},
        ],
        "hints": ["不要真的合并（那是 O(m+n)）", "在较短的数组上二分「分割线」的位置"],
        "funcName": "find_median_sorted_arrays",
        "testCases": [
            {"args": [[1, 3], [2]], "expect": 2.0},
            {"args": [[1, 2], [3, 4]], "expect": 2.5},
            {"args": [[], [1]], "expect": 1.0},
        ],
        "solutions": [
            {"name": "在较短数组上二分分割线", "time": "O(log min(m,n))", "space": "O(1)",
             "idea": "把两个数组各切一刀，左半部分总共 (m+n+1)/2 个元素。要保证「左半最大值 ≤ 右半最小值」。在较短的数组上二分这个切分位置即可。",
             "code": """def find_median_sorted_arrays(nums1, nums2):
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1
    m, n = len(nums1), len(nums2)
    total_left = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2          # nums1 左半元素个数
        j = total_left - i          # nums2 左半元素个数
        a_left = nums1[i - 1] if i > 0 else float('-inf')
        a_right = nums1[i] if i < m else float('inf')
        b_left = nums2[j - 1] if j > 0 else float('-inf')
        b_right = nums2[j] if j < n else float('inf')
        if a_left <= b_right and b_left <= a_right:
            if (m + n) % 2 == 1:
                return float(max(a_left, b_left))
            return (max(a_left, b_left) + min(a_right, b_right)) / 2.0
        elif a_left > b_right:
            hi = i - 1
        else:
            lo = i + 1
    return 0.0"""},
            {"name": "合并排序（简单直观）", "time": "O(m+n)", "space": "O(m+n)",
             "idea": "合并两个有序数组，直接取中位数。不满足 O(log) 要求，但最容易理解。",
             "code": """def find_median_sorted_arrays(nums1, nums2):
    a = sorted(nums1 + nums2)
    n = len(a)
    if n % 2 == 1:
        return float(a[n // 2])
    return (a[n // 2 - 1] + a[n // 2]) / 2.0"""},
        ],
    },
    {
        "slug": "search-rotated", "lcId": 33, "title": "搜索旋转排序数组",
        "difficulty": "中等", "tags": ["数组", "二分查找"], "category": "二分查找",
        "visualizer": "binary-search.html", "visHint": "二分的变体：判断哪半边是有序的",
        "desc": "整数数组 nums 按升序排列，数组中的值互不相同。在传递给函数之前，nums 在预先未知的某个下标 k 上进行了旋转。给你旋转后的数组 nums 和一个整数 target，如果 nums 中存在这个目标值 target，则返回它的下标，否则返回 -1。必须使用 O(log n) 的算法。",
        "examples": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4"},
            {"input": "nums = [4,5,6,7,0,1,2], target = 3", "output": "-1"},
        ],
        "hints": ["二分后总有一半是有序的", "先判断哪半边有序，再看 target 是否在那一半"],
        "funcName": "search_rotated",
        "testCases": [
            {"args": [[4, 5, 6, 7, 0, 1, 2], 0], "expect": 4},
            {"args": [[4, 5, 6, 7, 0, 1, 2], 3], "expect": -1},
            {"args": [[1], 0], "expect": -1},
            {"args": [[1], 1], "expect": 0},
        ],
        "solutions": [
            {"name": "二分 + 判断有序半边", "time": "O(log n)", "space": "O(1)",
             "idea": "取中点后，左半 [lo, mid] 和右半 [mid, hi] 中必有一半是有序的。判断出有序的那半，再看 target 是否落在它的范围内，据此收缩区间。",
             "code": """def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:          # 左半有序
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:                              # 右半有序
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1"""},
        ],
    },
    {
        "slug": "koko-bananas", "lcId": 875, "title": "爱吃香蕉的珂珂",
        "difficulty": "中等", "tags": ["数组", "二分查找", "二分答案"], "category": "二分查找",
        "visualizer": "binary-search.html", "visHint": "二分答案：在「速度」空间上二分",
        "desc": "珂珂喜欢吃香蕉。这里有 n 堆香蕉，第 i 堆中有 piles[i] 根香蕉。警卫已经离开了，将在 h 小时后回来。珂珂可以决定她吃香蕉的速度 k（单位：根/小时）。每个小时，她将会选择一堆香蕉，从中吃掉 k 根。如果这堆香蕉少于 k 根，她将吃掉这堆的所有香蕉，然后这一小时内不会再吃更多的香蕉。珂珂喜欢慢慢吃，但仍然想在警卫回来前吃掉所有香蕉。返回她可以在 h 小时内吃掉所有香蕉的最小速度 k。",
        "examples": [
            {"input": "piles = [3,6,7,11], h = 8", "output": "4"},
            {"input": "piles = [30,11,23,4,20], h = 5", "output": "30"},
        ],
        "hints": ["速度越快耗时越少（单调性）", "在 [1, max(piles)] 上二分速度"],
        "funcName": "min_eating_speed",
        "testCases": [
            {"args": [[3, 6, 7, 11], 8], "expect": 4},
            {"args": [[30, 11, 23, 4, 20], 5], "expect": 30},
            {"args": [[30, 11, 23, 4, 20], 6], "expect": 23},
        ],
        "solutions": [
            {"name": "二分答案", "time": "O(n log maxPile)", "space": "O(1)",
             "idea": "速度 k 越大，所需时间越少——具备单调性，可以二分。对每个候选 k，算出总耗时 hours_needed(k)，找满足 ≤ h 的最小 k。",
             "code": """def min_eating_speed(piles, h):
    def hours_needed(k):
        total = 0
        for p in piles:
            total += (p + k - 1) // k       # 向上取整
        return total

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= h:
            hi = mid
        else:
            lo = mid + 1
    return lo"""},
        ],
    },
]
