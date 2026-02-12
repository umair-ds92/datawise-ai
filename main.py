"""
DataWise AI - CLI Entry Point
Run data analysis from the command line
"""

import asyncio
import argparse
import sys
from pathlib import Path

from team.analyzer_gpt import create_basic_team
from config.openai_model_client import get_model_client
from config.docker_utils import (
    getDockerCommandLineExecutor,
    start_docker_container,
    stop_docker_container
)
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from utils.validators import validate_file, validate_task, validate_environment
from utils.logging import agent_logger
from utils.metrics import metrics_tracker
from utils.error_handlers import format_error_for_user


async def run_analysis(task: str, data_file: str = None):
    """
    Run multi-agent data analysis

    Args:
        task: Analysis task description
        data_file: Optional path to data file
    """
    model_client = get_model_client()
    docker = getDockerCommandLineExecutor()

    team = create_basic_team(docker, model_client)

    print("\n" + "="*60)
    print("🤖 DataWise AI - Starting Analysis")
    print("="*60)
    print(f"📋 Task: {task}")
    if data_file:
        print(f"📂 File: {data_file}")
    print("="*60 + "\n")

    agent_logger.log_task_start(task)
    metrics_tracker.start_task(task)

    try:
        await start_docker_container(docker)

        async for message in team.run_stream(task=task):
            print("-" * 40)
            if isinstance(message, TextMessage):
                print(f"[{message.source}]\n{message.content}")
                agent_logger.log_agent_message(message.source, message.content)

            elif isinstance(message, TaskResult):
                print(f"\n✅ Stop Reason: {message.stop_reason}")

        metrics_tracker.end_task(status='success')
        agent_logger.log_task_complete(task, 0)

        # Show metrics summary
        summary = metrics_tracker.get_session_summary()
        print("\n" + "="*60)
        print("📊 Session Summary")
        print("="*60)
        print(f"  Tasks completed : {summary['tasks_completed']}")
        print(f"  Total tokens    : {summary['total_tokens']:,}")
        print(f"  Total cost      : ${summary['total_cost_usd']:.4f}")
        print(f"  Duration        : {summary['total_duration_seconds']:.1f}s")
        print("="*60)

    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
        metrics_tracker.end_task(status='interrupted')

    except Exception as e:
        metrics_tracker.end_task(status='error')
        agent_logger.log_error(e, context='run_analysis')
        print(f"\n❌ Error: {format_error_for_user(e)}")
        return 1

    finally:
        await stop_docker_container(docker)

    return 0


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="DataWise AI - Multi-agent data analysis",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --task "How many rows in my data?"
  python main.py --task "Plot sales by month" --file data/sales.csv
  python main.py --interactive
        """
    )

    parser.add_argument(
        '--task', '-t',
        type=str,
        help='Analysis task to perform'
    )

    parser.add_argument(
        '--file', '-f',
        type=str,
        help='Path to data file (CSV, Excel, JSON)'
    )

    parser.add_argument(
        '--interactive', '-i',
        action='store_true',
        help='Run in interactive mode (ask multiple questions)'
    )

    return parser.parse_args()


async def interactive_mode():
    """Run in interactive mode - ask multiple questions"""
    print("\n" + "="*60)
    print("🤖 DataWise AI - Interactive Mode")
    print("="*60)
    print("Type your questions below. Type 'exit' to quit.\n")

    while True:
        try:
            task = input("📋 Your task: ").strip()

            if task.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break

            if not task:
                continue

            # Validate task
            is_valid, error_msg = validate_task(task)
            if not is_valid:
                print(f"❌ {error_msg}\n")
                continue

            await run_analysis(task)
            print()

        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break


def main():
    """Main entry point"""
    # Validate environment
    env_valid, missing = validate_environment()
    if not env_valid:
        print(f"❌ Missing required environment variables: {', '.join(missing)}")
        print("Please check your .env file.")
        sys.exit(1)

    args = parse_args()

    # Interactive mode
    if args.interactive:
        asyncio.run(interactive_mode())
        return

    # Single task mode
    if not args.task:
        print("❌ Please provide a task with --task or use --interactive mode")
        print("Run 'python main.py --help' for usage information")
        sys.exit(1)

    # Validate task
    is_valid, error_msg = validate_task(args.task)
    if not is_valid:
        print(f"❌ Invalid task: {error_msg}")
        sys.exit(1)

    # Handle file upload
    if args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"❌ File not found: {args.file}")
            sys.exit(1)

        is_valid, error_msg = validate_file(file_path.name, file_path.stat().st_size)
        if not is_valid:
            print(f"❌ Invalid file: {error_msg}")
            sys.exit(1)

        # Copy to temp directory
        import shutil
        Path('temp').mkdir(exist_ok=True)
        shutil.copy2(args.file, 'temp/data.csv')
        print(f"✅ File loaded: {args.file}")

    # Run analysis
    exit_code = asyncio.run(run_analysis(args.task, args.file))
    sys.exit(exit_code)


if __name__ == '__main__':
    main()