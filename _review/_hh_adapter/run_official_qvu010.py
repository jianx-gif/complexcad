"""Same as run_official.py but with qwen-vl-utils 0.0.10 (the version pinned in the cadrille
Dockerfile) loaded from the isolated folder pylib_qvu010, instead of the venv's 0.0.14.
With 0.0.14 process_vision_info returns a 2x3x336x336 tensor that the Qwen2-VL processor does
not resize again -> video grid 24x24 (144 tokens); with 0.0.10 it returns two 280x280 PIL
frames -> grid 20x20 (100 tokens), which is what the checkpoint was trained with."""
import sys, os
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, 'pylib_qvu010'))
import qwen_vl_utils  # noqa: E402
assert 'pylib_qvu010' in qwen_vl_utils.__file__, qwen_vl_utils.__file__
print('qwen_vl_utils from', qwen_vl_utils.__file__, flush=True)
sys.path.insert(0, HERE)
import run_official  # noqa: E402

if __name__ == '__main__':
    run_official.main()
